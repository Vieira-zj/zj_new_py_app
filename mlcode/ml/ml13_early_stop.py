# %%
# 数据
import numpy as np
np.random.seed(42)
m = 100
X = 6 * np.random.rand(m, 1) - 3
y = 2 + X + 0.5 * X**2 + np.random.randn(m, 1)
X.shape, y.shape

# %%
# 数据拆分
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(
    X[:50], y[:50].ravel(), test_size=0.5, random_state=10)
X_train.shape, y_train.shape

# %%
# 数据预处理，增加高阶属性，并归一化
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

poly_scaler = Pipeline([
    ('poly_features', PolynomialFeatures(degree=90, include_bias=False)),
    ('std_scaler', StandardScaler()),
])

X_train_poly_scaled = poly_scaler.fit_transform(X_train)
X_val_poly_scaled = poly_scaler.transform(X_val)
X_train_poly_scaled.shape, X_val_poly_scaled.shape

# %%
# 模型迭代
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error

sgd_reg = SGDRegressor(max_iter=1, penalty=None, eta0=0.0005,
                       warm_start=True, learning_rate='constant', random_state=42)

n_epochs = 500
train_errors, val_errors = [], []
for epoch in range(n_epochs):
    sgd_reg.fit(X_train_poly_scaled, y_train)
    y_train_predict = sgd_reg.predict(X_train_poly_scaled)
    y_val_predict = sgd_reg.predict(X_val_poly_scaled)
    train_errors.append(mean_squared_error(y_train_predict, y_train))
    val_errors.append(mean_squared_error(y_val_predict, y_val))

best_epoch = np.argmin(val_errors)
best_val_rmse = np.sqrt(val_errors[best_epoch])
best_epoch, best_val_rmse

# %%
%matplotlib inline
import matplotlib.pyplot as plt

# 做注释
plt.annotate('Best model', xy=(best_epoch, best_val_rmse), xytext=(best_epoch, best_val_rmse + 1),
             ha='center', arrowprops=dict(facecolor='black', shrink=0.05), fontsize=16,)

best_val_rmse -= 0.03  # just to make the graph look better
plt.plot([0, n_epochs], [best_val_rmse, best_val_rmse], 'k:', linewidth=2)
plt.plot(np.sqrt(val_errors), 'b-', linewidth=3, label='Validation set')
plt.plot(np.sqrt(train_errors), 'r--', linewidth=2, label='Training set')
plt.legend(loc='upper right', fontsize=14)
plt.xlabel('Epoch', fontsize=14)
plt.ylabel('RMSE', fontsize=14)
plt.show()


# %%
# 补充
x = np.random.rand(10, 1)
print(x.shape)
x

# %%
x.ravel()

# %%
y = np.random.rand(10)
print(y.shape)
y

# %%
np.sqrt([25, 36])

# %%
print('regression early stop demo done')
