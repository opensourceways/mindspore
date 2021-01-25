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
#include "tools/converter/parser/tf/tf_split_parser.h"
#include <string>
#include <memory>
#include <map>
#include <vector>
#include "tools/converter/parser/tf/tf_node_parser_registry.h"
#include "ops/split.h"

namespace mindspore {
namespace lite {
ops::PrimitiveC *TFSplitParser::Parse(const tensorflow::NodeDef &tf_op,
                                      const std::map<string, const tensorflow::NodeDef *> &tf_node_map,
                                      std::vector<std::string> *inputs, int *output_size) {
  auto primitive_c = new (std::nothrow) ops::Split;
  if (primitive_c == nullptr) {
    MS_LOG(ERROR) << "new Split failed";
    return nullptr;
  }

  tensorflow::AttrValue attr_value;
  if (!TensorFlowUtils::FindAttrValue(tf_op, "num_split", &attr_value)) {
    MS_LOG(ERROR) << "The attribute num_split should be specified";
    return nullptr;
  }
  auto numberSplit = attr_value.i();
  primitive_c->set_output_num(numberSplit);

  int split_dim_index = 2;
  int input_index = 0;
  if (tf_op.op() == "Split") {
    split_dim_index = 0;
    input_index = 1;
  }

  auto split_dim_node = GetConstInputNode(tf_node_map, tf_op.input(split_dim_index));
  if (split_dim_node == nullptr) {
    MS_LOG(ERROR) << "Find Split input split_dim node failed";
    return nullptr;
  }
  if (!TensorFlowUtils::FindAttrValue(*split_dim_node, "value", &attr_value)) {
    MS_LOG(ERROR) << "The attribute splitDim should be specified";
    return nullptr;
  }
  auto splitDim = attr_value.tensor().int_val(0);
  primitive_c->set_axis(splitDim);

  if (tf_op.op() == "SplitV") {
    auto size_splits_node = GetConstInputNode(tf_node_map, tf_op.input(1));
    if (size_splits_node == nullptr) {
      MS_LOG(ERROR) << "Find Split input size_splits failed";
      return nullptr;
    }
    if (!TensorFlowUtils::FindAttrValue(*size_splits_node, "value", &attr_value)) {
      MS_LOG(ERROR) << "The attribute size splits should be specified";
      return nullptr;
    }
    auto size_splits_tensor = attr_value.tensor();
    auto size = size_splits_tensor.tensor_content().size() / sizeof(int32_t);

    std::vector<int64_t> sizeSplits;
    sizeSplits.resize(size);
    auto ret = memcpy_s(sizeSplits.data(), size * sizeof(int32_t), size_splits_tensor.tensor_content().data(),
                        size * sizeof(int32_t));
    if (ret != EOK) {
      MS_LOG(ERROR) << "memcpy_s failed";
      return nullptr;
    }
    primitive_c->set_size_splits(sizeSplits);
  }

  *output_size = numberSplit;
  if (AddOpInput(tf_op, input_index, inputs) != RET_OK) {
    MS_LOG(ERROR) << "add op input failed";
    return nullptr;
  }

  return primitive_c;
}

TFNodeRegistrar g_tfSplitParser("Split", new TFSplitParser());
TFNodeRegistrar g_tfSplitVParser("SplitV", new TFSplitParser());
}  // namespace lite
}  // namespace mindspore
