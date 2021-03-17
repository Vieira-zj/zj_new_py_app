# %%
# 简单线性回归模型
import pandas as pd
import numpy as np
np.__version__

# %%
# 数据预处理
import os
data_path = os.path.join(
    os.getenv('PYPATH'), 'mlcode/ml/data/studentscores.csv')
dataset = pd.read_csv(data_path)
dataset.shape

# %%
# hours
X = dataset.iloc[:, : 1].values
X

# %%
# scores
Y = dataset.iloc[:, 1].values
Y

# %%
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=1/4, random_state=0)
X_train, X_test, Y_train, Y_test

# %%
# 训练集使用简单线性回归模型来训练
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor = regressor.fit(X_train, Y_train)
print('model train done')

# %%
# 预测结果
Y_pred = regressor.predict(X_test)
print(Y_pred.shape)
Y_pred

# %%
# 训练集结果可视化
import matplotlib.pyplot as plt
plt.scatter(X_train, Y_train, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')
plt.show()

# %%
# 测试集结果可视化
plt.scatter(X_test, Y_test, color='red')
plt.plot(X_test, regressor.predict(X_test), color='blue')
plt.show()

# %%
print('simple lr demo done')
