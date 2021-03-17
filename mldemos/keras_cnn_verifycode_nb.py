# %%
# 训练CNN模型 识别网站验证码
import numpy as np
import pandas as pd
import tensorflow.keras as keras
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

np.__version__, keras.__version__

# %%
# 读取数据
df = pd.read_csv('data/verifycode.csv')
df.shape

# %%
# 标签值
keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
        'G', 'H', 'J', 'K', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
label_dict = dict(zip(keys, range(len(keys))))
label_dict

# %%
x_data = df[['v' + str(i+1) for i in range(320)]]
y_data = pd.DataFrame({'label': df['label']})
y_data['class'] = y_data['label'].apply(lambda x: label_dict[x])

x_data.shape, y_data.shape

# %%
# 将数据分为训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    x_data, y_data['class'], test_size=0.3, random_state=42)
x_train = np.array(X_train).reshape((-1, 20, 16, 1))
x_test = np.array(X_test).reshape((-1, 20, 16, 1))

x_train.shape, x_test.shape

# %%
# 对标签值进行 one-hot encoding
n_classes = len(keys)
y_train = keras.utils.to_categorical(Y_train, n_classes)
y_test = keras.utils.to_categorical(Y_test, n_classes)

y_train.shape, y_test.shape

# %%
# CNN模型
model = keras.models.Sequential()

# 卷积层和池化层
input_shape = x_train[0].shape
model.add(keras.layers.Conv2D(32, kernel_size=(3, 3),
                              input_shape=input_shape, padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Conv2D(32, kernel_size=(3, 3), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
# Dropout层
model.add(keras.layers.Dropout(0.25))

model.add(keras.layers.Conv2D(64, kernel_size=(3, 3), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Conv2D(64, kernel_size=(3, 3), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
model.add(keras.layers.Dropout(0.25))

model.add(keras.layers.Conv2D(128, kernel_size=(3, 3), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Conv2D(128, kernel_size=(3, 3), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
model.add(keras.layers.Dropout(0.25))

model.add(keras.layers.Flatten())

# 全连接层
model.add(keras.layers.Dense(256, activation='relu'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dense(n_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.summary()

# %%
# keras.utils.plot_model(model, to_file='/tmp/test/model.png', show_shapes=True)
print('model plot saved.')

# %%
# 模型训练
batch_size = 64
n_epochs = 100
callbacks = [keras.callbacks.EarlyStopping(
    monitor='val_accuracy', patience=5, verbose=1)]
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=n_epochs,
                    verbose=1, validation_data=(x_test, y_test), callbacks=callbacks)
print('model train finished.')

# %%
model_path = '/tmp/test/verifycode_Keras.h5'
model.save(model_path)
print('model saved.')

# %%
# 绘制验证集上的准确率曲线
val_acc = history.history['val_accuracy']
plt.plot(range(len(val_acc)), val_acc, label='CNN model')
plt.title('Validation accuracy on verifycode dataset')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()

# %%
# 模型效果验证查看 => opencv_verifycode.py
print('keras cnn verifycode of chars demo done.')
