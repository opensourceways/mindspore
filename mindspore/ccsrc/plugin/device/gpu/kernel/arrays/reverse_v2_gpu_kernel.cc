/**
 * Copyright 2021-2022 Huawei Technologies Co., Ltd
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
#include "plugin/device/gpu/kernel/arrays/reverse_v2_gpu_kernel.h"
#include "plugin/device/gpu/kernel/cuda_impl/cuda_ops/complex.h"

namespace mindspore {
namespace kernel {
template <typename T>
using Complex = mindspore::utils::Complex<T>;
MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeComplex64).AddOutputAttr(kNumberTypeComplex64),
                      ReverseV2GpuKernelMod, Complex<float>)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeComplex128).AddOutputAttr(kNumberTypeComplex128),
                      ReverseV2GpuKernelMod, Complex<double>)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeFloat16).AddOutputAttr(kNumberTypeFloat16),
                      ReverseV2GpuKernelMod, half)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeFloat32).AddOutputAttr(kNumberTypeFloat32),
                      ReverseV2GpuKernelMod, float)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeUInt8).AddOutputAttr(kNumberTypeUInt8),
                      ReverseV2GpuKernelMod, uint8_t)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeInt16).AddOutputAttr(kNumberTypeInt16),
                      ReverseV2GpuKernelMod, int16_t)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeInt32).AddOutputAttr(kNumberTypeInt32),
                      ReverseV2GpuKernelMod, int32_t)

MS_REG_GPU_KERNEL_ONE(ReverseV2, KernelAttr().AddInputAttr(kNumberTypeInt64).AddOutputAttr(kNumberTypeInt64),
                      ReverseV2GpuKernelMod, int64_t)
}  // namespace kernel
}  // namespace mindspore
