/**
 * Copyright 2019-2021 Huawei Technologies Co., Ltd
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
#include "src/ops/populate/populate_register.h"
#include "src/common/log_adapter.h"
#include "src/tensor.h"
#include "nnacl/shape.h"

namespace mindspore {
namespace lite {

OpParameter *PopulateShapeParameter(const void *prim) {
  ShapeParameter *shape_param = reinterpret_cast<ShapeParameter *>(malloc(sizeof(ShapeParameter)));
  if (shape_param == nullptr) {
    MS_LOG(ERROR) << "malloc ShapeParameter failed.";
    return nullptr;
  }
  memset(shape_param, 0, sizeof(ShapeParameter));
  auto primitive = static_cast<const schema::Primitive *>(prim);
  shape_param->op_parameter_.type_ = primitive->value_type();
  return reinterpret_cast<OpParameter *>(shape_param);
}

Registry ShapeParameterRegistry(schema::PrimitiveType_Shape, PopulateShapeParameter, SCHEMA_CUR);
}  // namespace lite
}  // namespace mindspore
