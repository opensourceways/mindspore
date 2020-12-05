# Copyright 2020 Huawei Technologies Co., Ltd
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
"""Operators for random."""

from ..._checkparam import Validator, Rel
from ...common import dtype as mstype
from ..primitive import PrimitiveWithInfer, prim_attr_register
from .._utils import get_broadcast_shape


class StandardNormal(PrimitiveWithInfer):
    r"""
    Generates random numbers according to the standard Normal (or Gaussian) random number distribution.

    Args:
        seed (int): Random seed, must be non-negative. Default: 0.
        seed2 (int): Random seed2, must be non-negative. Default: 0.

    Inputs:
        - **shape** (tuple) - The shape of random tensor to be generated. Only constant value is allowed.

    Outputs:
        Tensor. The shape is the same as the input `shape`. The dtype is float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> shape = (4, 16)
        >>> stdnormal = ops.StandardNormal(seed=2)
        >>> output = stdnormal(shape)
        >>> result = output.shape
        >>> print(result)
        (4, 16)
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """Initialize StandardNormal"""
        self.init_prim_io_names(inputs=['shape'], outputs=['output'])
        Validator.check_non_negative_int(seed, "seed", self.name)
        Validator.check_non_negative_int(seed2, "seed2", self.name)

    def __infer__(self, shape):
        shape_v = shape["value"]
        if shape_v is None:
            raise ValueError(f"For {self.name}, shape must be const.")
        Validator.check_value_type("shape", shape_v, [tuple], self.name)
        for i, shape_i in enumerate(shape_v):
            Validator.check_positive_int(shape_i, f'shape[{i}]', self.name)
        out = {
            'shape': shape_v,
            'dtype': mstype.float32,
            'value': None}
        return out


class StandardLaplace(PrimitiveWithInfer):
    r"""
    Generates random numbers according to the Laplace random number distribution (mean=0, lambda=1).
    It is defined as:

    .. math::
        \text{f}(x;0,1) = \frac{1}{2}\exp(-|x|),

    Args:
        seed (int): Random seed. Default: 0.
        seed2 (int): Random seed2. Default: 0.

    Inputs:
        - **shape** (tuple) - The shape of random tensor to be generated. Only constant value is allowed.

    Outputs:
        Tensor. The shape that the input 'shape' denotes. The dtype is float32.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> shape = (4, 16)
        >>> stdlaplace = ops.StandardLaplace(seed=2)
        >>> output = stdlaplace(shape)
        >>> result = output.shape
        >>> print(result)
        (4, 16)
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """Initialize StandardLaplace"""
        self.init_prim_io_names(inputs=['shape'], outputs=['output'])
        Validator.check_value_type('seed', seed, [int], self.name)
        Validator.check_value_type('seed2', seed2, [int], self.name)

    def __infer__(self, shape):
        shape_v = shape["value"]
        if shape_v is None:
            raise ValueError(f"For {self.name}, shape must be const.")
        Validator.check_value_type("shape", shape_v, [tuple], self.name)
        for i, shape_i in enumerate(shape_v):
            Validator.check_positive_int(shape_i, f'shape[{i}]', self.name)
        out = {
            'shape': shape_v,
            'dtype': mstype.float32,
            'value': None}
        return out


class Gamma(PrimitiveWithInfer):
    r"""
    Produces random positive floating-point values x, distributed according to probability density function:

    .. math::
        \text{P}(x|α,β) = \frac{\exp(-x/β)}{{β^α}\cdot{\Gamma(α)}}\cdot{x^{α-1}},

    Args:
        seed (int): Random seed, must be non-negative. Default: 0.
        seed2 (int): Random seed2, must be non-negative. Default: 0.

    Inputs:
        - **shape** (tuple) - The shape of random tensor to be generated. Only constant value is allowed.
        - **alpha** (Tensor) - The α distribution parameter. It must be greater than 0.
          It is also known as the shape parameter with float32 data type.
        - **beta** (Tensor) - The β distribution parameter. It must be greater than 0.
          It is also known as the scale parameter with float32 data type.

    Outputs:
        Tensor. The shape must be the broadcasted shape of Input "shape" and shapes of alpha and beta.
        The dtype is float32.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> shape = (2, 2)
        >>> alpha = Tensor(1.0, mstype.float32)
        >>> beta = Tensor(1.0, mstype.float32)
        >>> gamma = ops.Gamma(seed=3)
        >>> output = gamma(shape, alpha, beta)
        >>> print(output)
        [[0.21962446 0.33740655]
         [1.0859369  0.25875127]]
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """Initialize Gamma"""
        self.init_prim_io_names(inputs=['shape', 'alpha', 'beta'], outputs=['output'])
        Validator.check_non_negative_int(seed, "seed", self.name)
        Validator.check_non_negative_int(seed2, "seed2", self.name)

    def __infer__(self, shape, alpha, beta):
        shape_v = shape["value"]
        if shape_v is None:
            raise ValueError(f"For {self.name}, shape must be const.")
        Validator.check_value_type("shape", shape_v, [tuple], self.name)
        for i, shape_i in enumerate(shape_v):
            Validator.check_positive_int(shape_i, f'shape[{i}]', self.name)
        Validator.check_tensor_dtype_valid("alpha", alpha["dtype"], [mstype.float32], self.name)
        Validator.check_tensor_dtype_valid("beta", beta["dtype"], [mstype.float32], self.name)
        broadcast_shape = get_broadcast_shape(alpha['shape'], beta['shape'], self.name)
        broadcast_shape = get_broadcast_shape(broadcast_shape, shape_v, self.name)
        out = {
            'shape': broadcast_shape,
            'dtype': mstype.float32,
            'value': None}
        return out


class Poisson(PrimitiveWithInfer):
    r"""
    Produces random non-negative integer values i, distributed according to discrete probability function:

    .. math::
        \text{P}(i|μ) = \frac{\exp(-μ)μ^{i}}{i!},

    Args:
        seed (int): Random seed, must be non-negative. Default: 0.
        seed2 (int): Random seed2, must be non-negative. Default: 0.

    Inputs:
        - **shape** (tuple) - The shape of random tensor to be generated. Only constant value is allowed.
        - **mean** (Tensor) - μ parameter the distribution was constructed with. The parameter defines mean number
          of occurrences of the event. It must be greater than 0. With float32 data type.

    Outputs:
        Tensor. Its shape must be the broadcasted shape of `shape` and the shape of `mean`.
        The dtype is int32.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> shape = (4, 16)
        >>> mean = Tensor(5.0, mstype.float32)
        >>> poisson = ops.Poisson(seed=5)
        >>> output = poisson(shape, mean)
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """Initialize Poisson"""
        self.init_prim_io_names(inputs=['shape', 'mean'], outputs=['output'])
        Validator.check_non_negative_int(seed, "seed", self.name)
        Validator.check_non_negative_int(seed2, "seed2", self.name)

    def __infer__(self, shape, mean):
        shape_v = shape["value"]
        if shape_v is None:
            raise ValueError(f"For {self.name}, shape must be const.")
        Validator.check_value_type("shape", shape_v, [tuple], self.name)
        for i, shape_i in enumerate(shape_v):
            Validator.check_positive_int(shape_i, f'shape[{i}]', self.name)
        Validator.check_tensor_dtype_valid("mean", mean["dtype"], [mstype.float32], self.name)
        broadcast_shape = get_broadcast_shape(mean['shape'], shape_v, self.name)
        out = {
            'shape': broadcast_shape,
            'dtype': mstype.int32,
            'value': None}
        return out


class UniformInt(PrimitiveWithInfer):
    r"""
    Produces random integer values i, uniformly distributed on the closed interval [minval, maxval), that is,
    distributed according to the discrete probability function:

    .. math::
        \text{P}(i|a,b) = \frac{1}{b-a+1},

    Note:
        The number in tensor minval must be strictly less than maxval at any position after broadcasting.

    Args:
        seed (int): Random seed, must be non-negative. Default: 0.
        seed2 (int): Random seed2, must be non-negative. Default: 0.

    Inputs:
        - **shape** (tuple) - The shape of random tensor to be generated. Only constant value is allowed.
        - **minval** (Tensor) - The distribution parameter, a.
          It defines the minimum possibly generated value, with int32 data type. Only one number is supported.
        - **maxval** (Tensor) - The distribution parameter, b.
          It defines the maximum possibly generated value, with int32 data type. Only one number is supported.

    Outputs:
        Tensor. The shape is the same as the input 'shape', and the data type is int32.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> shape = (2, 4)
        >>> minval = Tensor(1, mstype.int32)
        >>> maxval = Tensor(5, mstype.int32)
        >>> uniform_int = ops.UniformInt(seed=10)
        >>> output = uniform_int(shape, minval, maxval)
        >>> print(output)
        [[4 2 1 3]
         [4 3 4 5]]
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """Initialize UniformInt"""
        self.init_prim_io_names(inputs=['shape', 'minval', 'maxval'], outputs=['output'])
        Validator.check_non_negative_int(seed, "seed", self.name)
        Validator.check_non_negative_int(seed2, "seed2", self.name)

    def __infer__(self, shape, minval, maxval):
        shape_v = shape["value"]
        if shape_v is None:
            raise ValueError(f"For {self.name}, shape must be const.")
        Validator.check_value_type("shape", shape_v, [tuple], self.name)
        for i, shape_i in enumerate(shape_v):
            Validator.check_positive_int(shape_i, f'shape[{i}]', self.name)
        Validator.check_tensor_dtype_valid("minval", minval["dtype"], [mstype.int32], self.name)
        Validator.check_tensor_dtype_valid("maxval", maxval["dtype"], [mstype.int32], self.name)
        minval_shape = minval['shape']
        maxval_shape = maxval['shape']
        Validator.check("dim of minval", len(minval_shape), '0(scalar)', 0, Rel.EQ, self.name)
        Validator.check("dim of maxval", len(maxval_shape), '0(scalar)', 0, Rel.EQ, self.name)
        out = {
            'shape': shape_v,
            'dtype': mstype.int32,
            'value': None}
        return out


class UniformReal(PrimitiveWithInfer):
    r"""
    Produces random floating-point values i, uniformly distributed to the interval [0, 1).

    Args:
        seed (int): Random seed, must be non-negative. Default: 0.
        seed2 (int): Random seed2, must be non-negative. Default: 0.

    Inputs:
        - **shape** (tuple) - The shape of random tensor to be generated. Only constant value is allowed.

    Outputs:
        Tensor. The shape that the input 'shape' denotes. The dtype is float32.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> shape = (2, 2)
        >>> uniformreal = ops.UniformReal(seed=2)
        >>> output = uniformreal(shape)
        >>> print(output)
        [[0.4359949 0.18508208]
         [0.02592623 0.93154085]]
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """Initialize UniformReal"""
        self.init_prim_io_names(inputs=['shape'], outputs=['output'])
        Validator.check_non_negative_int(seed, "seed", self.name)
        Validator.check_non_negative_int(seed2, "seed2", self.name)

    def __infer__(self, shape):
        shape_v = shape["value"]
        if shape_v is None:
            raise ValueError(f"For {self.name}, shape must be const.")
        Validator.check_value_type("shape", shape_v, [tuple], self.name)
        for i, shape_i in enumerate(shape_v):
            Validator.check_positive_int(shape_i, f'shape[{i}]', self.name)
        out = {
            'shape': shape_v,
            'dtype': mstype.float32,
            'value': None}
        return out


class Randperm(PrimitiveWithInfer):
    """
    Generates random samples from 0 to n-1.

    Args:
        n (int): Number of items expected to get and the number must be greater than 0. Default: 1.
        dtype (mindspore.dtype): The type of output. Default: mindspore.int32.

    Outputs:
        - **output** (Tensor) - The output Tensor with shape :math:`(n,)` and type: dtype.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> randperm = ops.Randperm(20)
        >>> output = randperm()
        >>> print(output)
        [15 6 11 19 14 16 9 5 13 18 4 10 8 0 17 2 14 1 12 3 7]
    """

    @prim_attr_register
    def __init__(self, n=1, dtype=mstype.int32):
        """Initialize Randperm"""
        Validator.check_value_type("n", n, [int], self.name)
        self.dtype = dtype
        self.n = n
        self.init_prim_io_names(inputs=[], outputs=['output'])

    def infer_shape(self):
        Validator.check_int(self.n, 1, Rel.GE, "1", self.name)
        return [self.n]

    def infer_dtype(self):
        valid_values = (mstype.int8, mstype.int16, mstype.int32, mstype.int64,
                        mstype.uint8, mstype.uint16, mstype.uint32, mstype.uint64)
        Validator.check_type_name("dtype", self.dtype, valid_values, self.name)
        return self.dtype


class RandomChoiceWithMask(PrimitiveWithInfer):
    """
    Generates a random sample as index tensor with a mask tensor from a given tensor.

    The input must be a tensor of rank not less than 1. If its rank is greater than or equal to 2,
    the first dimension specifies the number of samples.
    The index tensor and the mask tensor have the fixed shapes. The index tensor denotes the index of the nonzero
    sample, while the mask tensor denotes which elements in the index tensor are valid.

    Args:
        count (int): Number of items expected to get and the number must be greater than 0. Default: 256.
        seed (int): Random seed. Default: 0.
        seed2 (int): Random seed2. Default: 0.

    Inputs:
        - **input_x** (Tensor[bool]) - The input tensor.
          The input tensor rank must be greater than or equal to 1 and less than or equal to 5.

    Outputs:
        Two tensors, the first one is the index tensor and the other one is the mask tensor.

        - **index** (Tensor) - The output shape is 2-D.
        - **mask** (Tensor) - The output shape is 1-D.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> rnd_choice_mask = ops.RandomChoiceWithMask()
        >>> input_x = Tensor(np.ones(shape=[240000, 4]).astype(np.bool))
        >>> output_y, output_mask = rnd_choice_mask(input_x)
        >>> result = output_y.shape
        >>> print(result)
        (256, 2)
        >>> result = output_mask.shape
        >>> print(result)
        (256,)
    """

    @prim_attr_register
    def __init__(self, count=256, seed=0, seed2=0):
        """Initialize RandomChoiceWithMask"""
        Validator.check_value_type("count", count, [int], self.name)
        Validator.check_positive_int(count, "count", self.name)
        Validator.check_value_type('seed', seed, [int], self.name)
        Validator.check_value_type('seed2', seed2, [int], self.name)

    def infer_shape(self, x_shape):
        Validator.check_int(len(x_shape), 1, Rel.GE, "input_x rank", self.name)
        Validator.check_int(len(x_shape), 5, Rel.LE, "input_x rank", self.name)
        return ([self.count, len(x_shape)], [self.count])

    def infer_dtype(self, x_dtype):
        Validator.check_tensor_dtype_valid('x', x_dtype, [mstype.bool_], self.name)
        return (mstype.int32, mstype.bool_)


class RandomCategorical(PrimitiveWithInfer):
    """
    Generates random samples from a given categorical distribution tensor.

    Args:
        dtype (mindspore.dtype): The type of output. Its value must be one of mindspore.int16,
            mindspore.int32 and mindspore.int64. Default: mindspore.int64.

    Inputs:
        - **logits** (Tensor) - The input tensor. 2-D Tensor with shape [batch_size, num_classes].
        - **num_sample** (int) - Number of sample to be drawn. Only constant values is allowed.
        - **seed** (int) - Random seed. Default: 0. Only constant values is allowed.

    Outputs:
        - **output** (Tensor) - The output Tensor with shape [batch_size, num_samples].

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> class Net(nn.Cell):
        ...   def __init__(self, num_sample):
        ...     super(Net, self).__init__()
        ...     self.random_categorical = ops.RandomCategorical(mindspore.int64)
        ...     self.num_sample = num_sample
        ...   def construct(self, logits, seed=0):
        ...     return self.random_categorical(logits, self.num_sample, seed)
        ...
        >>> x = np.random.random((10, 5)).astype(np.float32)
        >>> net = Net(8)
        >>> output = net(Tensor(x))
        >>> print(output)
        [[0 2 0 3 4 2 0 2]
         [0 2 1 3 4 2 0 2]
         [0 2 0 3 4 2 0 2]
         [0 2 1 3 4 2 0 2]
         [0 2 1 3 4 2 0 2]
         [0 2 1 3 4 2 0 2]
         [0 2 0 3 4 2 0 2]
         [0 2 0 3 4 2 0 2]
         [0 2 1 3 4 3 0 3]
         [0 2 1 3 4 2 0 2]]
    """

    @prim_attr_register
    def __init__(self, dtype=mstype.int64):
        """Initialize RandomCategorical"""
        self.dtype = dtype

        valid_values = (mstype.int32, mstype.int16, mstype.int64)
        Validator.check_type_name("dtype", dtype, valid_values, self.name)
        self.init_prim_io_names(inputs=['logits', 'num_samples', 'seed'],
                                outputs=['output'])

    def __infer__(self, logits, num_samples, seed):
        logits_dtype = logits['dtype']
        valid_dtypes = (mstype.float32, mstype.float16, mstype.float64)
        Validator.check_tensor_dtype_valid('logits', logits_dtype, valid_dtypes, self.name)
        num_samples_v = num_samples['value']
        seed_v = seed['value']
        Validator.check_value_type('num_samples', num_samples_v, (int,), self.name)
        Validator.check_value_type('seed', seed_v, (int,), self.name)
        Validator.check_positive_int(num_samples_v, "num_samples", self.name)
        x_shape = list(logits['shape'])
        if len(x_shape) != 2:
            raise ValueError("RandomCategorical shape should be 2-dimension.")
        ndim = len(x_shape) - 1
        x_shape[ndim] = num_samples_v
        self.add_prim_attr('num_samples', num_samples_v)
        self.add_prim_attr('seed', seed_v)
        return {'shape': (x_shape),
                'dtype': (self.dtype),
                'value': None}


class Multinomial(PrimitiveWithInfer):
    r"""
    Returns a tensor sampled from the multinomial probability distribution located in the corresponding
    row of tensor input.

    Note:
        The rows of input do not need to sum to one (in which case we use the values as weights),
        but must be non-negative, finite and have a non-zero sum.
    Args:
        seed (int): Random seed, must be non-negative. Default: 0.
        seed2 (int): Random seed2, must be non-negative. Default: 0.
    Inputs:
        - **input** (Tensor[float32]) - the input tensor containing the cumsum of probabilities, must be 1 or 2
          dimensions.
        - **num_samples** (int32) - number of samples to draw.

    Outputs:
        Tensor with the same rows as input, each row has num_samples sampled indices.

    Supported Platforms:
        ``GPU``

    Examples:
        >>> input = Tensor([0., 9., 4., 0.], mstype.float32)
        >>> multinomial = ops.Multinomial(seed=10)
        >>> output = multinomial(input, 2)
    """

    @prim_attr_register
    def __init__(self, seed=0, seed2=0):
        """init"""
        Validator.check_non_negative_int(seed, "seed", self.name)
        Validator.check_non_negative_int(seed2, "seed2", self.name)
        self.init_prim_io_names(inputs=['input', 'num_sample'], outputs=['output'])

    def __infer__(self, inputs, num_samples):
        input_shape = inputs["shape"]
        if len(input_shape) != 1 and len(input_shape) != 2:
            raise ValueError("input dim must be 1 or 2")
        Validator.check_tensor_dtype_valid('inputs', inputs['dtype'], [mstype.float32], self.name)
        num_samples_value = num_samples["value"]
        if num_samples_value is None:
            raise ValueError(f"For {self.name}, shape nust be const")
        Validator.check_value_type("num_samples", num_samples_value, (int,), self.name)
        Validator.check_positive_int(num_samples_value, "num_samples")
        y_shape = (num_samples_value,)
        if len(input_shape) == 2:
            y_shape = (input_shape[0], num_samples_value)
        out = {
            "shape": y_shape,
            "dtype": mstype.int32,
            "value": None}
        return out


class UniformCandidateSampler(PrimitiveWithInfer):
    r"""
    Uniform candidate sampler.

    This function samples a set of classes(sampled_candidates) from [0, range_max-1] based on uniform distribution.
    If unique=True, candidates are drawn without replacement, else unique=False with replacement.

    Args:
        num_true (int): The number of target classes in each training example.
        num_sampled (int): The number of classes to randomly sample. The sampled_candidates will have a shape
            of num_sampled. If unique=True, num_sampled must be less than or equal to range_max.
        unique (bool): Whether all sampled classes in a batch are unique.
        range_max (int): The number of possible classes, must be non-negative.
        seed (int): Used for random number generation, must be non-negative. If seed has a value of 0,
            seed will be replaced with a randomly generated value. Default: 0.
        remove_accidental_hits (bool): Whether accidental hit is removed. Default: False.

    Inputs:
        - **true_classes** (Tensor) - A Tensor. The target classes with a Tensor shape of (batch_size, num_true).

    Outputs:
        - **sampled_candidates** (Tensor) - The sampled_candidates is independent of the true classes.
          Shape: (num_sampled, ).
        - **true_expected_count** (Tensor) - The expected counts under the sampling distribution of each
          of true_classes. Shape: (batch_size, num_true).
        - **sampled_expected_count** (Tensor) - The expected counts under the sampling distribution of
          each of sampled_candidates. Shape: (num_sampled, ).

    Supported Platforms:
        ``GPU``

    Examples:
        >>> sampler = ops.UniformCandidateSampler(1, 3, False, 4)
        >>> output1, output2, output3 = sampler(Tensor(np.array([[1],[3],[4],[6],[3]], dtype=np.int32)))
        >>> print(output1, output2, output3)
        [1, 1, 3], [[0.75], [0.75], [0.75], [0.75], [0.75]], [0.75, 0.75, 0.75]
    """

    @prim_attr_register
    def __init__(self, num_true, num_sampled, unique, range_max, seed=0, remove_accidental_hits=False):
        """Initialize UniformCandidateSampler"""
        Validator.check_value_type("num_true", num_true, [int], self.name)
        Validator.check_value_type("num_sampled", num_sampled, [int], self.name)
        Validator.check_value_type("unique", unique, [bool], self.name)
        Validator.check_value_type("range_max", range_max, [int], self.name)
        Validator.check_value_type("seed", seed, [int], self.name)
        Validator.check_value_type("remove_accidental_hits", remove_accidental_hits, [bool], self.name)
        Validator.check("value of num_sampled", num_sampled, '', 0, Rel.GT, self.name)
        Validator.check("value of range_max", range_max, '', 0, Rel.GT, self.name)
        self.num_true = num_true
        if unique:
            Validator.check('value of num_sampled', num_sampled, "value of range_max", range_max, Rel.LE, self.name)
        Validator.check("value of seed", seed, '', 0, Rel.GE, self.name)
        self.num_sampled = num_sampled

    def infer_dtype(self, true_classes_type):
        Validator.check_tensor_dtype_valid("true_classes_type", true_classes_type, (mstype.int32), self.name)
        return (true_classes_type, mstype.float32, mstype.float32)

    def infer_shape(self, true_classes_shape):
        Validator.check("true_class.shape[1]", true_classes_shape[1], "num_true", self.num_true, Rel.EQ, self.name)
        return ([self.num_sampled], true_classes_shape, [self.num_sampled])


class LogUniformCandidateSampler(PrimitiveWithInfer):
    """
    Generates random labels with a log-uniform distribution for sampled_candidates.

    Random sampling a tensor of sampled classes from the range of integers [0, range_max).

    Args:
        num_true (int): The number of target classes per training example. Default: 1.
        num_sampled (int): The number of classes to randomly sample. Default: 5.
        unique (bool): Determines whether sample with rejection. If unique is True,
            all sampled classes in a batch are unique. Default: True.
        range_max (int): The number of possible classes. Default: 5.
        seed (int): Random seed, must be non-negative.

    Inputs:
        - **true_classes** (Tensor) - The target classes. With data type of int64 and shape [batch_size, num_true].

    Outputs:
        Tuple of 3 Tensors.

        - **sampled_candidates** (Tensor) - A Tensor with shape (num_sampled,) and the same type as `true_classes`.
        - **true_expected_count** (Tensor) - A Tensor with the same shape as `true_classes and` type float32.
        - **sampled_expected_count** (Tensor) - A Tensor with the same shape as `sampled_candidates` and type float32.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> sampler = ops.LogUniformCandidateSampler(1, 5, True, 5)
        >>> output1, output2, output3 = sampler(Tensor(np.array([[1, 7], [0, 4], [3, 3]])))
        >>> print(output1, output2, output3)
        [3, 2, 0, 4, 1],
        [[9.23129916e-01, 4.93363708e-01],
         [9.92489874e-01, 6.58063710e-01],
         [7.35534430e-01, 7.35534430e-01]],
        [7.35534430e-01, 8.26258004e-01, 9.92489874e-01, 6.58063710e-01, 9.23129916e-01]

    """

    @prim_attr_register
    def __init__(self, num_true=1, num_sampled=5, unique=True, range_max=5, seed=0):
        """Initialize LogUniformCandidateSampler"""
        self.init_prim_io_names(inputs=['true_classes'],
                                outputs=['sampled_candidates', 'true_expected_count', 'sampled_expected_count'])
        Validator.check_value_type("num_true", num_true, [int], self.name)
        Validator.check_value_type("num_sampled", num_sampled, [int], self.name)
        Validator.check_value_type("unique", unique, [bool], self.name)
        Validator.check_value_type("range_max", range_max, [int], self.name)
        Validator.check_value_type("seed", seed, [int], self.name)
        self.num_true = Validator.check_number("num_true", num_true, 1, Rel.GE, self.name)
        self.num_sampled = Validator.check_number("num_sampled", num_sampled, 1, Rel.GE, self.name)
        if unique:
            Validator.check_number("range_max", range_max, num_sampled, Rel.GE, self.name)
        self.range_max = range_max
        self.unique = unique
        self.seed = seed

    def infer_shape(self, true_classes_shape):
        Validator.check("true_classes shape rank", len(true_classes_shape), "expect", 2, Rel.EQ, self.name)
        Validator.check_int(true_classes_shape[1], self.num_true, Rel.EQ, 'true_classes_shape', self.name)
        return (self.num_sampled,), true_classes_shape, (self.num_sampled,)

    def infer_dtype(self, true_classes_type):
        Validator.check_subclass("true_classes_type", true_classes_type, mstype.tensor, self.name)
        valid_types = (mstype.int64,)
        Validator.check_tensor_dtype_valid("true_classes_type", true_classes_type, valid_types, self.name)
        expected_type = mstype.float32
        return true_classes_type, expected_type, expected_type
