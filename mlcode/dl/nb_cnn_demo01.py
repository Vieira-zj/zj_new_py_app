# pre-conditions:
# pip install notebook
# pip install tf-nightly
#
# mnist数据
# ${PIP_HOME}/tensorflow/python/keras/datasets/mnist.py 修改数据集path
# path = os.path.join(os.getenv('PYPATH'), 'mlcode/dl/data/mnist.npz')
#

# %%
import tensorflow as tf
import tensorflow.keras as keras

tf.__version__, tf.keras.__version__

# %%
# 导入手写数字集
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train.shape, y_train.shape, x_test.shape, y_test.shape

# %%
x_train[0]

# %%
# 数据集 数字图片
import matplotlib.pyplot as plt
%matplotlib inline
plt.imshow(x_train[0])
plt.show()

# %%
# 去色处理
plt.imshow(x_train[0], cmap=plt.cm.binary)
plt.show()

# %%
# 数据集 标签
y_train[0]

# %%
# 对数据进行缩放（将数据映射到 1-0 区间）
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
x_train[0]

# %%
plt.imshow(x_train[0], cmap=plt.cm.binary)
plt.show()

# %%
# 使用 Sequential 创建顺序执行神经网络
model = tf.keras.models.Sequential()
# 将多维数据压缩为一维数据，作为输入数据
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
# 添加两个神经层，因为每一层输入都是 128 而且激活函数使用简单的 relu
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
# 评价模型 指定 loss 函数类型
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
print('define a model')

# %%
# 开始训练
model.fit(x_train, y_train, epochs=3)
print('tf train done')
# 每完成一次所有 batch 运算就算为 epoch
# Epoch 1/3 loss: 0.2631 - accuracy: 0.9234
# Epoch 2/3 loss: 0.1072 - accuracy: 0.9668
# Epoch 3/3 loss: 0.0736 - accuracy: 0.9765

# %%
# 验证测试集 loss 和 acc
val_loss, val_acc = model.evaluate(x_test, y_test)
val_loss, val_acc

# %%
# 预测
predictions = model.predict(x_test)
print(predictions.shape)
predictions[0]

# %%
# 测试集中第一张数字图片的预测结果
import numpy as np
np.max(predictions[0]), np.argmax(predictions[0])

# %%
# 显示测试集中第一张数字图片
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.show()

# %%
# 保存模型
model.save('epic_num_reader.model')
# 加载保存的模型
new_model = tf.keras.models.load_model('epic_num_reader.model')
# 测试保存的模型
predictions = new_model.predict(x_test)
np.max(predictions[1]), np.argmax(predictions[1])

# %%
plt.imshow(x_test[1], cmap=plt.cm.binary)
plt.show()

# %%
print('tf cnn demo done')
