# %%
# 多元线性回归
import pandas as pd
import numpy as np
np.__version__

# %%
# 导入数据集
import os
data_path = os.path.join(
    os.getenv('PYPATH'), 'mlcode/ml/data/50_Startups.csv')
dataset = pd.read_csv(data_path)
dataset.shape, dataset.columns

# %%
X = dataset.iloc[:, :-1].values
X[:5]

# %%
# Profit
Y = dataset.iloc[:, 4].values
Y[:5]

# %%
# 将类别数据数字化
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder = LabelEncoder()
X[:, 3] = labelencoder.fit_transform(X[:, 3])
X[:5]

# %%
from sklearn.compose import ColumnTransformer
categorical_features = [3]
onehotencoder = OneHotEncoder()
clt = ColumnTransformer(
    [('name', onehotencoder, categorical_features)], remainder='passthrough')
X = clt.fit_transform(X)
X[:5]

# %%
# 躲避虚拟变量陷阱
X = X[:, 1:]

# %%
X[:5]

# %%
# 拆分数据集为训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=0)
X_test, Y_test

# %%
# 在训练集上训练多元线性回归模型
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, Y_train)
print('model train done')

# %%
# 在测试集上预测结果
y_pred = regressor.predict(X_test)
print('model predict done')

# %%
y_pred

# %%
print('multiple lr demo done')
