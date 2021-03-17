# %%
# K近邻法 (K-NN)
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
# 将数据划分成训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)
X_test.shape, y_test.shape

# %%
# 特征缩放
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train.shape, X_test.shape

# %%
print(X_train[:, 0].min(), X_train[:, 0].max())
print(X_train[:, 1].min(), X_train[:, 1].max())

# %%
# 使用K-NN对训练集数据进行训练
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
classifier.fit(X_train, y_train)
print('knn train done')

# %%
# 对测试集进行预测
y_pred = classifier.predict(X_test)
print(y_pred.shape)
print(np.sum(y_pred == 1))
y_pred[:5]

# %%
# 生成混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

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
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
plt.contourf(X1, X2, classifier.predict(Z).reshape(X1.shape),
             alpha=0.75, cmap=ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c=ListedColormap(('red', 'green'))(i), label=j)

plt.title('KNN(Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# %%
print('ml knn demo done')
