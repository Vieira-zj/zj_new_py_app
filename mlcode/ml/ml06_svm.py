# %%
# 支持向量机 (SVM)
import numpy as np
import pandas as pd
np.__version__

# %%
# 导入数据
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
y = dataset.iloc[:, 4].values
y[:5]

# %%
# 拆分数据集为训练集合和测试集合
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)
X_test.shape, y_test.shape

# %%
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)
X_train.shape, X_test.shape

# %%
print(X_train[:, 0].min(), X_train[:, 0].max())
print(X_train[:, 1].min(), X_train[:, 1].max())

# %%
# 适配SVM到训练集合
from sklearn.svm import SVC
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train, y_train)
print('svm train done')

# %%
y_pred = classifier.predict(X_test)
print(y_pred.shape)
print(np.sum(y_pred == 1))
y_pred[:5]

# %%
# 创建混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

# %%
# 训练集合结果可视化
X_set, y_set = X_train, y_train
X_min0 = X_set[:, 0].min() - 1
X_max0 = X_set[:, 0].max() + 1
X_min1 = X_set[:, 1].min() - 1
X_max1 = X_set[:, 1].max() + 1
X_min0, X_max0, X_min1, X_max1

# %%
X1, X2 = np.meshgrid(np.arange(start=X_min0, stop=X_max0, step=0.01),
                     np.arange(start=X_min1, stop=X_max1, step=0.01))
X1.shape, X2.shape

# %%
Z = np.array([X1.ravel(), X2.ravel()])
Z.shape

# %%
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
plt.contourf(X1, X2, classifier.predict(Z.T).reshape(X1.shape),
             alpha=0.75, cmap=ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green'))(i), label=j)

plt.title('SVM (Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# %%
# 测试集合结果可视化
X_set, y_set = X_test, y_test
X_min0 = X_set[:, 0].min() - 1
X_max0 = X_set[:, 0].max() + 1
X_min1 = X_set[:, 1].min() - 1
X_max1 = X_set[:, 1].max() + 1
X_min0, X_max0, X_min1, X_max1

# %%
X1, X2 = np.meshgrid(np.arange(start=X_min0, stop=X_max0, step=0.01),
                     np.arange(start=X_min1, stop=X_max1, step=0.01))
Z = np.array([X1.ravel(), X2.ravel()])

plt.contourf(X1, X2, classifier.predict(Z.T).reshape(X1.shape),
             alpha=0.75, cmap=ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green'))(i), label=j)

plt.title('SVM (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# %%
print('ml svm demo done')


# %%
# 补充：扁平化函数 ravel()
arr1 = np.arange(0, 6).reshape(2, 3)
arr2 = np.arange(10, 16).reshape(2, 3)
arr = np.array([arr1.ravel(), arr2.ravel()])
print(arr.shape)
arr

# %%
arr = arr.T
print(arr.shape)
arr

# %%
print('scikit-learn demo done')
