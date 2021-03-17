# %%
import numpy as np
np.random.seed(6)
np.__version__

# %%
# Broadcasting
a = np.array([0, 1, 2])
b = np.array([5, 5, 5])
a + b

# %%
x = np.ones((3, 3))
a + x


# %%
# newaxis 添加新的维度
x = np.random.randint(1, 8, size=5)
x

# %%
x[np.newaxis, :]

# %%
x.reshape(1, -1)

# %%
x[:, np.newaxis]

# %%
x.reshape(-1, 1)

# %%
# x and y have 50 steps from 0 to 5
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 50)[:, np.newaxis]
z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

%matplotlib inline
import matplotlib.pyplot as plt
plt.imshow(z, origin='lower', extent=[0, 5, 0, 5], cmap='viridis')
plt.colorbar()


# %%
# Comparison operators
x = np.array([1, 2, 3, 4, 5])
cond = x < 3
cond

# %%
print(np.count_nonzero(cond))
print(np.sum(cond))

# %%
(x * 2) == (x ** 2)

# %%
rnd = np.random.RandomState(0)
y = rnd.randint(10, size=(3, 4))
y

# %%
cond = y < 6
cond

# %%
y[cond]

# %%
print(np.sum(cond))
print(np.sum(cond, axis=1))

# %%
np.all(y < 8, axis=1)

# %%
z = np.arange(10)
cond = (z > 4) & (z < 8)
cond

# %%
z[cond]


# %%
# Indexing
rand = np.random.RandomState(42)
x = rand.randint(100, size=10)
x

# %%
idx = [3, 7, 4]
x[idx]

# %%
idx = np.array([[3, 7], [4, 5]])
x[idx]

# %%
y = np.arange(12).reshape((3, 4))
y

# %%
row = np.array([0, 1, 2])
col = np.array([2, 1, 3])
y[row, col]

# %%
y[2, [2, 0, 1]]

# %%
# modifying values with indexing
x = np.arange(10)
i = np.array([2, 1, 8, 4])
x[i] = 99
x

# %%
x[i] -= 10
x

# %%
print('numpy demo done')
