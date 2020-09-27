/**
 * Copyright 2020 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "runtime/device/cpu/kernel_select_cpu.h"

#include <string>
#include <memory>
#include <algorithm>

#include "backend/kernel_compiler/cpu/cpu_kernel_factory.h"

namespace mindspore {
namespace device {
namespace cpu {
using AnfAlgo = mindspore::session::AnfRuntimeAlgorithm;
using mindspore::kernel::KernelBuildInfo;
namespace {
bool IsInputNotCNode(const CNodePtr &kernel_node, size_t input_index) {
  auto input_node = AnfAlgo::VisitKernel(kernel_node->input(input_index + 1), 0).first;
  MS_EXCEPTION_IF_NULL(input_node);
  if (input_node->isa<Parameter>() || input_node->isa<ValueNode>()) {
    return true;
  }
  return false;
}

void UpdatePrevNotCNodeFormatDtype(const KernelAttr &kernel_attr, const std::vector<size_t> &input_not_cnode_indexes,
                                   const CNodePtr kernel_node) {
  for (auto &input_index : input_not_cnode_indexes) {
    auto input_node = AnfAlgo::VisitKernel(kernel_node->input(input_index + 1), 0).first;
    MS_EXCEPTION_IF_NULL(input_node);
    std::vector<TypeId> output_types;
    output_types.emplace_back(kernel_attr.GetInputAttr(input_index).first);
    auto builder = std::make_shared<kernel::KernelBuildInfo::KernelBuildInfoBuilder>();
    MS_EXCEPTION_IF_NULL(builder);
    builder->SetOutputsFormat({kOpFormat_DEFAULT});
    builder->SetOutputsDeviceType(output_types);
    AnfAlgo::SetSelectKernelBuildInfo(builder->Build(), input_node.get());
  }
}

void GetInputFormatsAndDtypes(const CNodePtr &kernel_node, std::vector<std::string> *input_formats,
                              std::vector<TypeId> *input_types, std::vector<size_t> *input_no_cnode_indexes) {
  size_t input_num = AnfAlgo::GetInputTensorNum(kernel_node);
  for (size_t input_index = 0; input_index < input_num; ++input_index) {
    TypeId dtype = kTypeUnknown;
    if (IsInputNotCNode(kernel_node, input_index)) {
      input_no_cnode_indexes->emplace_back(input_index);
      dtype = AnfAlgo::GetPrevNodeOutputInferDataType(kernel_node, input_index);
    } else {
      dtype = AnfAlgo::GetPrevNodeOutputDeviceDataType(kernel_node, input_index);
    }
    input_formats->emplace_back(kOpFormat_DEFAULT);
    input_types->emplace_back(dtype);
  }
}

void GetOutputFormatsAndDtypes(const CNodePtr &kernel_node, const KernelAttr &kernel_attr,
                               std::vector<std::string> *output_formats, std::vector<TypeId> *output_types) {
  size_t output_num = AnfAlgo::GetOutputTensorNum(kernel_node);
  for (size_t output_index = 0; output_index < output_num; ++output_index) {
    output_formats->emplace_back(kernel_attr.GetOutputAttr(output_index).second);
    auto dtype = kernel_attr.GetOutputAttr(output_index).first;
    output_types->emplace_back(dtype);
  }
}

std::pair<int, int> GetInputDtypeFormatMatchedNum(const KernelAttr &kernel_attr,
                                                  const std::vector<std::string> &input_formats,
                                                  const std::vector<TypeId> &input_types,
                                                  const std::vector<size_t> &input_not_cnode_indexes) {
  if (kernel_attr.GetInputSize() != input_types.size()) {
    MS_LOG(DEBUG) << "required input num:" << kernel_attr.GetInputSize() << ", actual input num:" << input_types.size();
    return std::make_pair(0, 0);
  }
  int data_type_matched_num = 0;
  int format_matched_num = 0;
  auto input_num = input_types.size();
  for (size_t i = 0; i < input_num; ++i) {
    bool is_not_cnode_idx = std::any_of(input_not_cnode_indexes.begin(), input_not_cnode_indexes.end(),
                                        [i](size_t index) { return index == i; });
    bool have_cnode_input = (input_types.size() != input_not_cnode_indexes.size());
    if (have_cnode_input && is_not_cnode_idx) {
      data_type_matched_num++;
      format_matched_num++;
      continue;
    }
    if (kernel_attr.GetInputAttr(i).first != input_types[i]) {
      MS_LOG(DEBUG) << "required dtype:" << kernel_attr.GetInputAttr(i).first
                    << ", actual input dtype:" << input_types[i];
    } else {
      data_type_matched_num++;
    }
    if (kernel_attr.GetInputAttr(i).second != input_formats[i]) {
      MS_LOG(DEBUG) << "required format:" << kernel_attr.GetInputAttr(i).second
                    << ", actual input format:" << input_formats[i];
    } else {
      format_matched_num++;
    }
  }
  return std::make_pair(data_type_matched_num, format_matched_num);
}

void ExpandKernelAttr(const CNodePtr &kernel_node, KernelAttr *kernel_attr) {
  MS_EXCEPTION_IF_NULL(kernel_attr);
  TypeId input_dtype = kernel_attr->GetInputAttr(0).first;
  size_t input_num = AnfAlgo::GetInputTensorNum(kernel_node);
  for (size_t i = 1; i < input_num; ++i) {
    kernel_attr->AddInputAttr(input_dtype);
  }

  TypeId output_dtype = kernel_attr->GetOutputAttr(0).first;
  size_t output_num = AnfAlgo::GetOutputTensorNum(kernel_node);
  for (size_t i = 1; i < output_num; ++i) {
    kernel_attr->AddOutputAttr(output_dtype);
  }
}

void SetKernelBuildInfo(const std::vector<std::string> &input_formats, const std::vector<TypeId> &input_types,
                        const std::vector<std::string> &output_formats, const std::vector<TypeId> &output_types,
                        AnfNode *kernel_node) {
  auto builder = std::make_shared<kernel::KernelBuildInfo::KernelBuildInfoBuilder>();
  MS_EXCEPTION_IF_NULL(builder);
  builder->SetInputsFormat(input_formats);
  builder->SetInputsDeviceType(input_types);
  builder->SetOutputsFormat(output_formats);
  builder->SetOutputsDeviceType(output_types);
  AnfAlgo::SetSelectKernelBuildInfo(builder->Build(), kernel_node);
}
}  // namespace

void SetKernelInfo(const CNodePtr &kernel_node) {
  std::vector<std::string> input_formats;
  std::vector<TypeId> input_types;
  std::vector<size_t> input_not_cnode_indexes;
  std::vector<std::string> output_formats;
  std::vector<TypeId> output_types;
  MS_LOG(INFO) << "SetKernelInfo, CNode Name: " << AnfAlgo::GetCNodeName(kernel_node);
  GetInputFormatsAndDtypes(kernel_node, &input_formats, &input_types, &input_not_cnode_indexes);
  auto kernel_attrs =
    kernel::CPUKernelFactory::GetInstance().GetSupportedKernelAttrList(AnfAlgo::GetCNodeName(kernel_node));
  if (kernel_attrs.empty()) {
    MS_LOG(EXCEPTION) << "Operator[" << AnfAlgo::GetCNodeName(kernel_node) << "] is not support.";
  }
  int max_type_matched_num = -1;
  int max_format_matched_num = -1;
  KernelAttr selected_kernel_attr;
  for (auto kernel_attr : kernel_attrs) {
    if (kernel_attr.GetAllSame()) {
      ExpandKernelAttr(kernel_node, &kernel_attr);
    }
    size_t output_num = AnfAlgo::GetOutputTensorNum(kernel_node);
    if (kernel_attr.GetOutputSize() != output_num) {
      MS_LOG(DEBUG) << "Output num is not equal!";
      continue;
    }
    std::pair<int, int> input_type_format_matched_num =
      GetInputDtypeFormatMatchedNum(kernel_attr, input_formats, input_types, input_not_cnode_indexes);
    // Data type first
    if (input_type_format_matched_num.first > max_type_matched_num) {
      max_type_matched_num = input_type_format_matched_num.first;
      max_format_matched_num = input_type_format_matched_num.second;
      selected_kernel_attr = kernel_attr;
    } else if (input_type_format_matched_num.first == max_type_matched_num &&
               input_type_format_matched_num.second > max_format_matched_num) {
      max_format_matched_num = input_type_format_matched_num.second;
      selected_kernel_attr = kernel_attr;
    }
    // All formats and data types matched
    if (max_type_matched_num == SizeToInt(input_types.size()) &&
        max_format_matched_num == SizeToInt(input_types.size())) {
      break;
    }
  }

  if (selected_kernel_attr.GetInputSize() > 0 && ((max_type_matched_num == SizeToInt(input_types.size()) &&
                                                   max_format_matched_num == SizeToInt(input_types.size())) ||
                                                  input_types.size() == input_not_cnode_indexes.size())) {
    MS_LOG(INFO) << "Input format and dtype is matched, max_type_matched_num: " << max_type_matched_num
                 << ", max_format_matched_num: " << max_format_matched_num;
    GetOutputFormatsAndDtypes(kernel_node, selected_kernel_attr, &output_formats, &output_types);
    UpdatePrevNotCNodeFormatDtype(selected_kernel_attr, input_not_cnode_indexes, kernel_node);
    for (auto &input_index : input_not_cnode_indexes) {
      input_types[input_index] = selected_kernel_attr.GetInputAttr(input_index).first;
    }
  }
  SetKernelBuildInfo(input_formats, input_types, output_formats, output_types, kernel_node.get());
}
}  // namespace cpu
}  // namespace device
}  // namespace mindspore
