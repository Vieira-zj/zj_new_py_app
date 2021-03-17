# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin

tensorflow board web:
$ tensorboard --logdir /tf/tf_scripts/logs
'''

import tensorflow as tf
import numpy as np
import os


def tensorflow_world():
    welcome = tf.constant('Welcome to TensorFlow world!')
    # run the session
    with tf.Session() as sess:
        print('output:', sess.run(welcome))


def tensorflow_math_op():
    FLAGS = tf.app.flags.FLAGS
    if not os.path.isabs(os.path.expanduser(FLAGS.log_dir)):
        raise ValueError('You must assign absolute path for log_dir')

    # define some constant values
    a = tf.constant(5.0, name='a')
    b = tf.constant(10.0, name='b')

    # some basic operations
    x = tf.add(a, b, name='add')
    y = tf.div(a, b, name='divide')

    # shape=[2,1]
    a1 = tf.constant([0.7, 0.9], name='a')
    b1 = tf.constant([1.0, 0.2], name='b')
    c = tf.add(a, b, name='add')
    print(c)

    with tf.Session() as sess:
        writer = tf.summary.FileWriter(os.path.expanduser(FLAGS.log_dir), sess.graph)

        print('a =', sess.run(a))
        print('b =', sess.run(b))
        print('a + b =', sess.run(x))
        print('a/b =', sess.run(y))
        # print('output:', sess.run([a, b, x, y]))
        # output: [5.0, 10.0, 15.0, 0.5]

        print('c = ', sess.run(c))

    if writer is not None:
        writer.close()


def tensorflow_placeholder():
    # 1
    a = tf.placeholder(tf.float16)
    b = tf.placeholder(tf.float16)
    c = tf.placeholder(tf.float16)

    d = tf.add(a, b)
    e = tf.multiply(d, c)
    f = tf.pow(e, 2, name='pow')
    g = tf.divide(f, a, name='divide')
    h = tf.sqrt(g, name='sqrt')

    with tf.Session() as sess:
        feed_dict = {a: 1, b: 2, c: 3}
        print('output:', sess.run(h, feed_dict=feed_dict))

    # 2
    # x = tf.constant([1, 2, 3, 4, 5, 6], shape=[2, 3])
    # y = tf.constant([7, 8, 9, 10, 11, 12], shape=[3, 2])
    x = tf.placeholder(tf.float32, shape=(2, 3))
    y = tf.placeholder(tf.float32, shape=(3, 2))
    z = tf.matmul(x, y)  # 矩阵x乘以矩阵y
    print('z:', z)

    with tf.Session() as sess:
        rand_x = np.array([1, 2, 3, 4, 5, 6]).reshape(2, 3)
        rand_y = np.array([7, 8, 9, 10, 11, 12]).reshape(3, 2)
        print('output:', sess.run(z, feed_dict={x: rand_x, y: rand_y}))


if __name__ == '__main__':

    # logs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    logs_path = os.path.join(os.getcwd(), 'logs')
    print('events log path:', logs_path)
    desc = 'Directory where event logs are written to.'
    tf.app.flags.DEFINE_string('log_dir', logs_path, desc)

    # tensorflow_world()
    # tensorflow_math_op()
    tensorflow_placeholder()

    print('tensorflow world DONE!')
