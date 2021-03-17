# %%
# 逻辑回归
import numpy as np
import pandas as pd
np.__version__

# %%
# STEP1: 数据预处理
# 导入数据集
import os
data_path = os.path.join(
    os.getenv('PYPATH'), 'mlcode/ml/data/Social_Network_Ads.csv')
dataset = pd.read_csv(data_path)
dataset.shape, dataset.columns

# %%
# Age, EstimatedSalary
X = dataset.iloc[:, [2, 3]].values
X[:5]

# %%
# Purchased (label)
Y = dataset.iloc[:, 4].values
Y[:5]

# %%
# 将数据集分成训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.25, random_state=0)
X_test.shape, y_test.shape

# %%
print('before Scaler')
print(X_test[:, 0].min(), X_test[:, 0].max())
print(X_test[:, 1].min(), X_test[:, 1].max())

# %%
# 特征缩放
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train[:5], X_test[:5]

# %%
print('after Scaler')
print(X_test[:, 0].min(), X_test[:, 0].max())
print(X_test[:, 1].min(), X_test[:, 1].max())

# %%
# STEP2: 逻辑回归模型 
# 
# 将逻辑回归应用于训练集
# 该项工作的库将会是一个线性模型库，之所以被称为线性是因为逻辑回归是一个线性分类器，
# 这意味着我们在二维空间中，我们两类用户（购买和不购买）将被一条直线分割。
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
print('lr train done')

# %%
# STEP3: 预测
# 预测测试集结果
y_pred = classifier.predict(X_test)
print(y_pred.shape)
print(np.sum(y_pred == 1))
y_pred[:5]

# %%
# STEP4: 评估预测
# 生成混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

# %%
# 训练集可视化
X_set, y_set = X_train, y_train
min_0 = X_set[:, 0].min()-1
max_0 = X_set[:, 0].max()+1
min_1 = X_set[:, 1].min()-1
max_1 = X_set[:, 1].max()+1
min_0, max_0, min_1, max_1

# %%
X1, X2 = np.meshgrid(np.arange(start=min_0, stop=max_0, step=0.01),
                     np.arange(start=min_1, stop=max_1, step=0.01))
X1.shape, X2.shape

# %%
Z = np.array([X1.ravel(), X2.ravel()]).T
Z.shape

# %%
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
plt.contourf(X1, X2, classifier.predict(Z).reshape(X1.shape),
             alpha=0.75, cmap=ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    print('i=%d, j=%d' % (i, j))
    # age as X, salary as Y
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green'))(i), label=j)

plt.title('LOGISTIC(Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# %%
# 测试集可视化
X_set, y_set = X_test, y_test
min_0 = X_set[:, 0].min()-1
max_0 = X_set[:, 0].max()+1
min_1 = X_set[:, 1].min()-1
max_1 = X_set[:, 1].max()+1
min_0, max_0, min_1, max_1

# %%
X1, X2 = np.meshgrid(np.arange(start=min_0, stop=max_0, step=0.01),
                     np.arange(start=min_1, stop=max_1, step=0.01))
X1.shape, X2.shape

# %%
Z = np.array([X1.ravel(), X2.ravel()]).T
Z.shape

# %%
plt.contourf(X1, X2, classifier.predict(Z).reshape(X1.shape),
             alpha=0.75, cmap=ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green'))(i), label=j)

plt.title('LOGISTIC(Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# %%
print('ml logistic lr demo done')


# %%
# 补充：plt.contour, plt.contourf
import numpy as np
x = np.array([1, 2])
y = np.array([1, 2])
z = np.array([[1, 2], [2, 3]])
np.unique(z)

# %%
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

plt.xlim(1, 2)
plt.ylim(1, 2)
colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
cmap = ListedColormap(colors[:len(np.unique(z))])
plt.contour(x,y,z,cmap=cmap)
# contourf 填充等高线之间的空隙颜色
# plt.contourf(x, y, z, cmap=cmap)
plt.show()

# %%
print('scikit-learn demo done')
