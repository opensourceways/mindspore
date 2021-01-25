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
 * distributed under the License is distributed on an AS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "tools/converter/parser/tflite/tflite_addn_parser.h"
#include <vector>
#include <memory>
#include "ops/addn.h"

namespace mindspore {
namespace lite {
ops::PrimitiveC *TfliteAddNParser::Parse(const std::unique_ptr<tflite::OperatorT> &tflite_op,
                                         const std::unique_ptr<tflite::ModelT> &tflite_model) {
  auto prim = new (std::nothrow) ops::AddN();
  if (prim == nullptr) {
    MS_LOG(ERROR) << "new AddN failed";
    return nullptr;
  }

  return prim;
}

TfliteNodeRegister g_tfliteAddNParser(tflite::BuiltinOperator_ADD_N, new TfliteAddNParser());
}  // namespace lite
}  // namespace mindspore
