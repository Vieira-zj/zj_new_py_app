# %%
import cv2
import numpy as np

import tensorflow as tf
import tensorflow.keras as keras

tf.__version__, keras.__version__

# %%
def resize_without_deformation(image, size=(100, 100)):
    '''
    不能暴力的resize成100*100, 否则会引起图片的变形。
    这里采用了一种手段就是将较短的一侧涂黑，使它变成和目标图像相同的比例，然后再resize.
    '''
    height, width, _ = image.shape
    longest_edge = max(height, width)
    top, bottom, left, right = 0, 0, 0, 0
    if height < longest_edge:
        height_diff = longest_edge - height
        top = int(height_diff / 2)
        bottom = height_diff - top
    elif width < longest_edge:
        width_diff = longest_edge - width
        left = (width_diff / 2)
        right = width_diff - left

    image_with_border = cv2.copyMakeBorder(
        image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0.0, 0])
    resized_image = cv2.resize(image_with_border, size)
    return resized_image

# %%
def read_image(size=None):
    data_x, data_y = [], []
    for i in range(177):
        try:
            im = cv2.imread('jm/s%s.bmp' % str(i))
            if size is None:
                size = (100, 100)
            im = resize_without_deformation(im, size)
            data_x.append(np.asarray(im, dtype=np.int8))
            data_y.append(str(int((i-1)/11.0)))
        except IOError as e:
            print(e)
        except:
            print('Unknow Error!')

    return data_x, data_y

# %%
IMAGE_SIZE = 100

size = (IMAGE_SIZE, IMAGE_SIZE)
raw_images, raw_labels = read_image(size)
raw_images, raw_labels = np.asarray(
    raw_images, dtype=np.float32), np.asarray(raw_labels)

# %%
from sklearn.model_selection import train_test_split

# 标签平等化
ont_hot_labels = keras.utils.to_categorical(raw_labels)

# 数据集拆分
train_x, valid_x, train_y, valid_y = train_test_split(
    raw_images, ont_hot_labels, test_size=0.3)

# 归一化
train_x /= 255.0
train_y /= 255.0

# %%
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.optimizers import SGD

face_model = keras.Sequential()

# 引进卷积和池化层，卷积类似于图像处理中的特征提取操作，池化则很类似于降维
face_model.add(Conv2D(32, 3, 3, border_mode='valid', subsample=(
    1, 1), dim_ordering='tf', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), activation='relu'))
face_model.add(Conv2D(32, 3, 3, border_mode='valid', subsample=(
    1, 1), dim_ordering='tf', activation='relu'))

face_model.add(MaxPooling2D(pool_size=(2, 2)))

# Dropout用来在训练时按一定概率随机丢弃一些神经元，以获得更高的训练速度以及防止过拟合
face_model.add(Dropout(0.2))

# Flatten用于卷积层与全连接层之间
face_model.add(Flatten())

# 全连接层
face_model.add(Dense(512, activation='relu'))
face_model.add(Dropout(0.4))

# 输出层
face_model.add(Dense(len(ont_hot_labels[0]), activation='sigmoid'))
face_model.summary()

# %%
# SGD（梯度下降优化器）来使损失函数最小化
learning_rate = 0.01
sgd_optimizer = SGD(lr=learning_rate, decay=1e-6, momentum=0.8, nesterov=True)

# 编译模型
face_model.compile(loss='categorical_crossentropy',
                   optimizer=sgd_optimizer, metrics=['accuracy'])

# 训练
face_model.fit(train_x, train_y, epochs=100, batch_size=20,
               shuffle=True, validation_data=(valid_x, valid_y))

# %%
# 评估结果
print(face_model.evaluate(valid_x, valid_y, verbose=0))

# 保存模型
MODEL_PATH = 'face_model.h5'
face_model.save(MODEL_PATH)


# %%
# 人脸识别
import cv2
import numpy as np
import tensorflow.keras as keras
from keras.models import load_model

# 加载卷积神经网络模型
MODEL_PATH = 'face_model.h5'
face_model = keras.Sequential()
face_model = load_model(MODEL_PATH)

# 打开摄像头，获取图片并灰度化
cap = cv2.VideoCapture(0)
ret, image = cap.read()
face = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# %%
# 无形变resize, 送入模型运算
img = resize_without_deformation(face)

img = img.reshape((1, 100, 100, 3))
img = np.asarray(img, dtype=np.float32)
img /= 255.0

face_model.predict_classes(img)

# %%
print('tf cnn demo done')
