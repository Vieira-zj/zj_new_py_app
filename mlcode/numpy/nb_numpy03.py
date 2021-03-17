# %%
import numpy as np
np.random.seed(6)
np.__version__

# %%
# Selecting random points
mean = [0, 0]
cov = [[1, 2], [2, 5]]
X = rand.multivariate_normal(mean, cov, 100)
print(X.shape)

%matplotlib inline
import matplotlib.pyplot as plt
import seaborn

seaborn.set()  # for plot styling
plt.scatter(X[:, 0], X[:, 1])

# %%
indices = np.random.choice(X.shape[0], 20, replace=False)
print(indices)
selection = X[indices]
print(selection.shape)

plt.scatter(X[:, 0], X[:, 1], alpha=0.3)
plt.scatter(selection[:, 0], selection[:, 1], facecolor='none', s=200)


# %%
# Sorting arrays
x = np.array([2, 1, 4, 3, 5])
np.sort(x)

# %%
i = np.argsort(x)
x[i]

# %%
# sorting along rows or columns
rand = np.random.RandomState(42)
X = rand.randint(0, 10, (4, 6))
X

# %%
np.sort(X, axis=0)

# %%
np.sort(X, axis=1)

# %%
X = rand.rand(10, 2)
print(X.shape)
plt.scatter(X[:, 0], X[:, 1], s=100)


# %%
# Structured arrays
data = np.zeros(4, dtype={'names': ('name', 'age', 'weight'),
                          'formats': ('U10', 'i4', 'f8')})
name = ['Alice', 'Bob', 'Cathy', 'Doug']
age = [25, 45, 37, 19]
weight = [55.0, 85.5, 68.0, 61.5]
data['name'] = name
data['age'] = age
data['weight'] = weight
data

# %%
# get all names
data['name']

# %%
# get first row of data
data[0]

# %%
# get name of last row
print(data[-1]['name'])

# get names where age is under 30
data[data['age'] < 30]['name']


# %%
# 补充
# meshgrid (生成坐标矩阵X,Y)
import numpy as np
import matplotlib.pyplot as plt

# 网格点的横纵坐标列向量
x = np.array([0, 2, 4])
y = np.array([1, 3])
X, Y = np.meshgrid(x, y)
print(X.shape, Y.shape)
X, Y

# %%
plt.plot(X, Y, color='red', marker='.', linestyle='')
plt.grid(True)
plt.show()


# %%
# flatten,ravel（将多维数组降位一维）
# flatten() 返回一份copy, 对copy所做的修改不会影响原始矩阵
# ravel() 返回的是view, 会影响原始矩阵
x = np.array([[1, 2], [3, 4], [5, 6]])
x.ravel()

# %%
x.reshape(-1)

# %%
print('numpy demo done')
