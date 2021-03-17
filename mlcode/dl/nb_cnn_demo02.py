# pre-conditions:
# pip install opencv-python
# pip install tqdm
#
# PetImages 目录 猫和狗的图像
# https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip
#

# %%
# PART1: 数据集操作
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm

np.__version__, cv2.__version__

# %%
DATADIR = os.path.join(
    os.getenv('HOME'), 'Downloads/tmp_files/ml_data/PetImages')
CATEGORIES = ['Dog', 'Cat']
img_array = None

for category in CATEGORIES:
    path = os.path.join(DATADIR, category)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path, img),
                               cv2.IMREAD_GRAYSCALE)
        break
    break
img_array.shape

# %%
plt.imshow(img_array, cmap='gray')
plt.show()

# %%
# 图像变小 灰度
IMG_SIZE = 50
new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
plt.show()

# %%
IMG_SIZE = 100
new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
plt.show()

# %%
new_array.shape

# %%
# 创建培训数据
training_data = []

def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)  # 得到分类，其中 0=dog 1=cat

        for img in tqdm(os.listdir(path)):
            try:
                img_array = cv2.imread(os.path.join(
                    path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # 大小转换
                training_data.append([new_array, class_num])  # 加入训练数据中
            except Exception as _:  # 为了保证输出是整洁的
                pass
            #except OSError as e:
            #    print('OSErrroBad img most likely', e, os.path.join(path,img))
            #except Exception as e:
            #    print('general exception', e, os.path.join(path,img))

# 确保数据是平衡（相同数量的狗和猫）
create_training_data()
len(training_data)

# %%
for sample in training_data[:10]:
    print(sample[1])

# %%
# 引入随机
import random
random.shuffle(training_data)
for sample in training_data[:10]:
    print(sample[1])

# %%
X = []
y = []
for features, label in training_data:
    X.append(features)
    y.append(label)
len(X), X[0].shape, len(y)

# %%
# print(X[0].reshape(-1, IMG_SIZE, IMG_SIZE, 1))
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
X.shape

# %%
y = np.array(y)
y.shape

# %%
# 保存数据（序列化）
import pickle
SAVEDIR = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/ml_data')
pickle_out = open(os.path.join(SAVEDIR, 'X.pickle'), 'wb')
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open(os.path.join(SAVEDIR, 'y.pickle'), 'wb')
pickle.dump(y, pickle_out)
pickle_out.close()
print('data dump done')


# %%
# PART2: 模型训练
import time
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard

tf.__version__, tf.keras.__version__

# %%
import pickle
SAVEDIR = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/ml_data')
pickle_in = open(os.path.join(SAVEDIR, 'X.pickle'), 'rb')
X = pickle.load(pickle_in)
pickle_in = open(os.path.join(SAVEDIR, 'y.pickle'), 'rb')
y = pickle.load(pickle_in)
X.shape, y.shape

# %%
# 归一化处理
X = X / 255.0

# %%
model = Sequential()

model.add(Conv2D(256, (3, 3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# this converts our 3D feature maps to 1D feature vectors
model.add(Flatten())

model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.summary()

# %%
NAME = 'Cats-vs-dogs-CNN'
tensorboard = TensorBoard(log_dir=os.path.join(
    SAVEDIR, 'logs/{}'.format(NAME)))

model.fit(X, y,
          batch_size=32,
          epochs=10,
          validation_split=0.3,
          callbacks=[tensorboard])
print('opencv train done')


# %%
# PART3: 验证与预测
# TODO:


# %%
# 补充
arr = np.arange(0, 4).reshape(2, 2)
arr

# %%
x = arr.reshape(-1, 2, 2, 1)
print(x.shape)
x

# %%
x / 2

# %%
print('opencv and tf cnn demo done')
