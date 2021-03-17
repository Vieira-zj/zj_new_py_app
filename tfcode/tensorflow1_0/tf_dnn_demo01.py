# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin
'''

import tensorflow as tf
import numpy as np
import os


def logistic_regression_01():
    # 输入层（2个特征）
    x = np.arange(4, dtype=np.float32).reshape(2, 2)
    y_ = np.array([0, 1], dtype=np.float32).reshape(2, 1)

    # 隐藏层（2个输入特征w, 3个神经元）
    # 节点1: a11=x1*w11+x2*w21+b
    # 节点2: a12=x1*w12+x2*w22+b
    # 节点3: a13=x1*w13+x2*w23+b
    w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
    b1 = tf.Variable(tf.zeros([3]))
    a = tf.nn.relu(tf.matmul(x, w1) + b1)
    print('a_shape:', a.shape)  # [2,3]

    # 输出层（3个输入特征w和1个神经元）
    # y = a11*w1+a12*w2+a13*w3+b
    w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))
    b2 = tf.Variable(tf.zeros([1]))
    y = tf.matmul(a, w2) + b2
    print('y_shape:', y.shape)  # [2,1]

    # 损失函数与训练
    cost = tf.nn.sigmoid_cross_entropy_with_logits(logits=y, labels=y_, name=None)
    train_op = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

    # run session
    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)
        for i in range(100):
            sess.run(train_op)

        print('w1:', sess.run(w1))
        print('w2:', sess.run(w2))
        print('y:', sess.run(y))
        print('y_:', y_)


def logistic_regression_02():
    # 输入数据
    x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
    # print(x_data.shape)  # [300, 1]
    noise = np.random.normal(0, 0.05, x_data.shape)
    y_data = np.square(x_data)-0.5+noise

    # 输入层（1个神经元）
    xs = tf.placeholder(tf.float32, [None, 1])
    ys_ = tf.placeholder(tf.float32, [None, 1])

    # 隐藏层（10个神经元）
    W1 = tf.Variable(tf.random_normal([1, 10]))
    b1 = tf.Variable(tf.zeros([1, 10])+0.1)
    # 激活函数tf.nn.relu
    a = tf.nn.relu(tf.matmul(xs, W1) + b1)
    print('a shape:', a.shape)  # [*, 10]

    # 输出层（1个神经元）
    W2 = tf.Variable(tf.random_normal([10, 1]))
    b2 = tf.Variable(tf.zeros([1, 1])+0.1)
    ys = tf.matmul(a, W2) + b2
    print('y shape:', ys.shape)  # [*, 1]

    # 损失函数和训练
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-ys_), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # run session
    saver = tf.train.Saver()
    model_dir = '/tf/tf_scripts/model'

    with tf.Session() as sess:
        if os.path.exists(os.path.join(model_dir, 'checkpoint')):
            print('session restore from model checkpoint.')
            # 从模型中恢复变量
            saver.restore(sess, os.path.join(model_dir, 'model.ckpt'))
        else:
            print('run session from init.')
            init = tf.global_variables_initializer()
            sess.run(init)

        # 训练1000次
        for i in range(1000):
            feed_dict = {xs: x_data, ys: y_data}
            _, loss_val = sess.run([train_step, loss], feed_dict=feed_dict)

            if(i % 50 == 0):
                print('loss:', loss_val)
                # 每50次epoch保存一次模型
                save_path = saver.save(sess, os.path.join(model_dir, 'model.ckpt'))
# logistic_regression


if __name__ == '__main__':

    logistic_regression_01()
    # logistic_regression_02()
    print('tensorflow logistic expression DONE!')
