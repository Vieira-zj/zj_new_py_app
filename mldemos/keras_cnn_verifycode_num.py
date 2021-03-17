'''
Created on 2020-06-12
@author: zhengjin
@desc:
1. 直接对验证码进行标记
2. 搭建 CNN 模型对标记好的数据集进行训练
3. 对新验证码进行预测
'''

import os
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.keras as keras

characters = '0123456789'
width, height, n_len, n_class = 50, 22, 4, 10

in_dir = 'data/verifycode_numbers'
out_dir = '/tmp/test'


def gen(dir, batch_size=32):
    '''
    产生训练的一批图片, 默认是32张图片
    '''
    X = np.zeros((batch_size, height, width, 3), dtype=np.uint8)
    y = [np.zeros((batch_size, n_class), dtype=np.uint8) for _ in range(n_len)]

    files = [f for f in os.listdir(dir) if os.path.isfile(
        os.path.join(dir, f)) and f.find('png') > 0]

    while True:
        for i in range(batch_size):
            path = random.choice(files)
            image_pixel = cv2.imread(os.path.join(dir, path), 1)
            X[i] = image_pixel

            filename = path[:4]
            for j, ch in enumerate(filename):
                y[j][i, :] = 0
                y[j][i, characters.find(ch)] = 1

        yield X, y


def plot_train_history(history, train_metrics, val_metrics):
    '''
    绘制损失值图像
    '''
    plt.plot(history.history.get(train_metrics), '-o')
    plt.plot(history.history.get(val_metrics), '-o')
    plt.ylabel(train_metrics)
    plt.xlabel('Epochs')
    plt.legend(['train', 'validation'])


def model_train_main():
    '''
    CNN模型训练
    '''
    input_tensor = keras.layers.Input((height, width, 3))
    x = input_tensor

    # 产生有4个block的卷积神经网络
    for i in range(4):
        # 卷积层
        x = keras.layers.Conv2D(32 * 2 ** i, (3, 3),
                                activation='relu', padding='same')(x)
        x = keras.layers.Conv2D(32 * 2 ** i, (3, 3),
                                activation='relu', padding='same')(x)
        # 池化层
        x = keras.layers.MaxPooling2D((2, 2))(x)

    x = keras.layers.Flatten()(x)
    x = keras.layers.Dropout(0.25)(x)

    # 多输出模型, 使用了4个 softmax 來分别预测4个字母的输出
    x = [keras.layers.Dense(n_class, activation='softmax',
                            name='c%d' % (i + 1))(x) for i in range(4)]

    model = keras.models.Model(inputs=input_tensor, outputs=x)
    model.summary()

    # 保存模型结构图
    # keras.utils.plot_model(model, to_file=os.path.join(
    #     out_dir, 'model.png'), show_shapes=True)

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta', metrics=['accuracy'])

    # 保存效果最好的模型
    cbks = [keras.callbacks.ModelCheckpoint(
        os.path.join(out_dir, 'best_model.h5'), save_best_only=True)]

    history = model.fit_generator(gen(in_dir, batch_size=8),  # 每次生成器会产生8张小批量的图片
                                  steps_per_epoch=120,  # 每次的epoch要训练120批图片
                                  epochs=50,  # 总共训练50次
                                  callbacks=cbks,  # 保存最好的模型
                                  validation_data=gen(in_dir),  # 验证数据也是用生成器来产生
                                  validation_steps=10)  # 用10组图片来进行验证

    # 输出整体的train loss与validation loss, 并保存图片
    plot_train_history(history, 'loss', 'val_loss')
    plt.savefig(os.path.join(out_dir, 'all_loss.png'))

    plt.figure(figsize=(12, n_len))
    # 4个数字, 输出每个数字的正确率
    for i in range(1, n_len+1):
        plt.subplot(2, 2, i)
        plot_train_history(history, 'c%d_accuracy' % i, 'val_c%d_accuracy' % i)
    # 保存图片
    plt.savefig(os.path.join(out_dir, 'train.png'))


def model_predict_main():
    '''
    使用训练好的CNN模型对新图片进行预测
    '''
    model = keras.models.load_model(os.path.join(out_dir, 'best_model.h5'))

    batch_size = 10
    X = np.zeros((batch_size, height, width, 3), dtype=np.uint8)
    for i in range(batch_size):
        in_path = os.path.join(in_dir, 'new_image/code%d.png' % (i+1))
        image_pixel = cv2.imread(in_path, 1)
        X[i] = image_pixel

    y_pred = model.predict(X)
    y_pred = np.argmax(y_pred, axis=2)

    # 输出每张验证码的预测结果
    for i in range(batch_size):
        print('predict result for code%d: ' % (i+1), end='')
        print(''.join(map(str, y_pred[:, i].tolist())))


if __name__ == '__main__':

    model_train_main()
    # model_predict_main()

    print('keras cnn verifycode of numbers demo done.')
