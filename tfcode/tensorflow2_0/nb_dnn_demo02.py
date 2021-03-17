# %%
import tensorflow as tf
from tensorflow.keras import layers
tf.__version__, tf.keras.__version__

# %%
# 构建模型
model = tf.keras.Sequential()
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))
print('define layers of model')

# %%
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=[tf.keras.metrics.categorical_accuracy])
model.summary()

# %%
# 模型训练
import numpy as np
np.random.seed(66)

train_x = np.random.random((1000, 72))
train_y = np.random.random((1000, 10))
val_x = np.random.random((200, 72))
val_y = np.random.random((200, 10))

model.fit(train_x, train_y, epochs=10, batch_size=100,
          validation_data=(val_x, val_y))
print('model train by np array')

# %%
model.fit(train_x, train_y, epochs=10, batch_size=100,
          validation_split=0.2)
print('model train and validation_split')

# %%
# 使用tf.data构建训练输入
dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
dataset = dataset.batch(32)
dataset = dataset.repeat()
val_dataset = tf.data.Dataset.from_tensor_slices((val_x, val_y))
val_dataset = val_dataset.batch(32)
val_dataset = val_dataset.repeat()

model.fit(dataset, epochs=10, steps_per_epoch=30,
          validation_data=val_dataset, validation_steps=3)
print('model train by tf dataset')

# %%
# 评估与预测
test_x = np.random.random((1000, 72))
test_y = np.random.random((1000, 10))
model.evaluate(test_x, test_y, batch_size=32)
print('modle evaluate by np array')

# %%
test_data = tf.data.Dataset.from_tensor_slices((test_x, test_y))
test_data = test_data.batch(32).repeat()
model.evaluate(test_data, steps=30)
print('modle evaluate by tf dataset')

# %%
result = model.predict(test_x, batch_size=32)
print(result.shape)
result[0]

# %%
print('tf keras demo done')
