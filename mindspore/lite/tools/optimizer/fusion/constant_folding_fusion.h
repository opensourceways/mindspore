/**
 * Copyright 2020-2021 Huawei Technologies Co., Ltd
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

#ifndef MINDSPORE_LITE_SRC_PASS_FUSION_CONSTANT_FOLDING_FUSION_H_
#define MINDSPORE_LITE_SRC_PASS_FUSION_CONSTANT_FOLDING_FUSION_H_

#include <set>
#include <utility>
#include <memory>
#include "backend/optimizer/common/pass.h"
#include "include/api/context.h"
#include "include/registry/parser_context.h"
#include "src/inner_context.h"
#include "tools/optimizer/graph/node_infershape.h"

namespace mindspore {
namespace opt {
class ConstFoldPass : public Pass {
 public:
  explicit ConstFoldPass(converter::FmkType fmk_type = converter::kFmkTypeMs, bool train_flag = false)
      : Pass("ConstFoldPass"), fmk_type_(fmk_type), train_flag_(train_flag) {}
  ~ConstFoldPass() override = default;
  bool Run(const FuncGraphPtr &func_graph) override;

 private:
  bool Init(const FuncGraphPtr &func_graph);
  int HandleCommonFold(const FuncGraphPtr &func_graph, std::set<FuncGraphPtr> *has_visited);
  bool CheckCanCommonFold(const CNodePtr &cnode) const;
  int HandleSpecialFold(const FuncGraphPtr &func_graph);
  bool CheckCanSpecialFold(const CNodePtr &cnode) const;
  int DoConstantFold(const FuncGraphPtr &func_graph, const CNodePtr &cnode) const;
  converter::FmkType fmk_type_{converter::kFmkTypeMs};
  bool train_flag_{false};
  std::shared_ptr<lite::InnerContext> context_{nullptr};
  std::shared_ptr<mindspore::Context> ms_context_{nullptr};
  std::shared_ptr<NodeInferShape> node_infershape_{nullptr};
};
}  // namespace opt
}  // namespace mindspore
#endif  // MINDSPORE_LITE_SRC_PASS_FUSION_CONSTANT_FOLDING_FUSION_H_
