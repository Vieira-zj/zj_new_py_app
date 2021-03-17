# %%
# dnn for y = 2 * x - 1
import tensorflow as tf
import numpy as np
from tensorflow import keras
tf.__version__, keras.__version__

# %%
# 创建一个具有1层的神经网络，该层具有1个神经元
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
# 损失函数 mean_squared_error
# 损失函数将猜测的答案与已知的正确答案进行比较，并衡量其结果的好坏
# 机器学习模型还需要优化器函数。根据损失函数的运行情况，它将尝试使损失最小化
model.compile(optimizer='sgd', loss='mean_squared_error')
model.summary()

# %%
# 模型将尝试500次迭代优化它的权重
xs = np.array([-1.0,  0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)
model.fit(xs, ys, epochs=100)

# %%
pred = model.predict([10.0])
pred

# %%
print('tf keras demo done')
