# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""NMSWithMask op"""
from mindspore.ops.op_info_register import op_info_register, AiCPURegOp, DataType

nms_with_mask_op_info = AiCPURegOp("NMSWithMask") \
    .fusion_type("OPAQUE") \
    .input(0, "box_scores", "required") \
    .output(0, "selected_boxes", "required") \
    .output(1, "selected_idx", "required") \
    .output(2, "selected_mask", "required") \
    .attr("iou_threshold", "float") \
    .dtype_format(DataType.F32_Default, DataType.F32_Default, DataType.I32_Default, DataType.BOOL_Default) \
    .get_op_info()


@op_info_register(nms_with_mask_op_info)
def _nms_with_mask_aicpu():
    """NMSWithMask AiCPU register"""
    return
