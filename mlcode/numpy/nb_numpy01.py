# %%
import numpy as np
np.random.seed(0)
np.__version__

# %%
# Create numpy ndarray
# integer array
np.array([1, 4, 2, 5, 3])

# %%
np.array([1, 2, 3, 4], dtype='float32')

# %%
# create a length-10 integer array filled with zeros
np.zeros(10, dtype=int)

# %%
# create a 3*5 floating-point array filled with ones
np.ones((3, 5), dtype=float)

# %%
# create a 3*5 array filled with 3.14
np.full((3, 5), 3.14)

# %%
# create an array of 5 values evenly spaced between 0 and 1
np.linspace(0, 1, 5)

# %%
# create a 3*3 array of uniformly distributed
# random values between 0 and 1
np.random.random((3, 3))

# %%
# create a 3*3 array of normally distributed random values
# with mean 0 and standard deviation 1
np.random.normal(0, 1, (3, 3))

# %%
# create a 3*3 array of random integers in the interval [0, 10)
np.random.randint(0, 10, (3, 3))


# %%
# Numpy array attributes
# two-dimensional array
arr = np.random.randint(10, size=(3, 4))
print(type(arr))
arr

# %%
print('ndim:', arr.ndim)
print('shape:', arr.shape)
print('size:', arr.size)
print('dtype:', arr.dtype)
print('nbytes:', arr.nbytes, 'bytes')


# %%
# Array slicing: accessing subarrays
# two rows, three columns
arr[:2, :3]

# %%
# first column of array
arr[:, 0]

# %%
# first row of array
arr[0, :]

# %%
# equivalent to arr[0, :]
arr[0]


# %%
# Concatenation of arrays
x = np.array([1, 2, 3])
y = np.array([3, 2, 1])
z = np.concatenate([x, y])
print(z.shape)
z

# %%
# concatenate along the first axis
grid = np.arange(6).reshape(2, 3)
grid

# %%
z = np.concatenate([grid, grid])
print(z.shape)
z

# %%
# concatenate along the second axis (zero-indexed)
z = np.concatenate([grid, grid], axis=1)
print(z.shape)
z


# %%
# Splitting of arrays
grid = np.arange(16).reshape((4, 4))
grid

# %%
upper, lower = np.vsplit(grid, [2])
upper, lower

# %%
left, right = np.hsplit(grid, [2])
left, right


# %%
# Array arithmetic
x = np.arange(4)
x

# %%
np.add(x, 2)

# %%
# absolute value
x = np.array([-2, -1, 0, 1, 2])
np.abs(x)

# %%
# aggregates
x = np.arange(1, 6)
np.add.reduce(x)

# %%
np.add.accumulate(x)

# %%
# summing values in an array
arr = np.arange(1, 6)
np.sum(arr)

# %%
big_array = np.random.rand(1000000)
%timeit sum(big_array)
%timeit np.sum(big_array)

# %%
# minimum and maximum
print(np.min(big_array))
print(np.max(big_array))

# %%
arr = np.random.random((3, 4))
arr

# %%
print(np.min(arr, axis=0))
print(np.max(arr, axis=1))


# %%
# 补充 reshape(-1)
x = np.arange(9).reshape(3, 3)
x

# %%
y = x.reshape(-1, 1)
y

# %%
z = y.reshape(-1)
z

# %%
# 补充 分桶
arr = np.arange(100)
counts, bin_edges = np.histogram(arr, bins=5)
counts, bin_edges

# %%
# 补充 np.newaxis
arrx = np.arange(10)
arrx[:, np.newaxis] + np.arange(4)

# %%
arrx = np.arange(4)
arrx[:, np.newaxis] * arrx

# %%
print('numpy demo done')
