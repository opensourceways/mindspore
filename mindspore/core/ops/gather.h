/**
 * Copyright 2021 Huawei Technologies Co., Ltd
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

#ifndef MINDSPORE_CORE_OPS_GATHER_H_
#define MINDSPORE_CORE_OPS_GATHER_H_
#include <map>
#include <vector>
#include <string>
#include <memory>
#include "ops/primitive_c.h"
#include "abstract/abstract_value.h"
#include "utils/check_convert_utils.h"

namespace mindspore {
namespace ops {
constexpr auto kNameGather = "Gather";
class MS_CORE_API Gather : public PrimitiveC {
 public:
  Gather() : PrimitiveC(kNameGather) { InitIOName({"param", "indices", "axis"}, {"output"}); }
  ~Gather() = default;
  MS_DECLARE_PARENT(Gather, PrimitiveC);
  void Init() {}
};
using PrimGatherPtr = std::shared_ptr<Gather>;
}  // namespace ops
}  // namespace mindspore

#endif  // MINDSPORE_CORE_OPS_GATHER_H_
