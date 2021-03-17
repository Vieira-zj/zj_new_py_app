# -*- coding: utf-8 -*-
'''
Created on 2019-05-19
@author: zhengjin

tensorflow board web:
$ tensorboard --logdir /tf/tf_scripts/lr_summary
'''

import numpy as np
import tensorflow as tf


def linear_regression_01():
    # data
    x = tf.placeholder(tf.float32)
    y_ = tf.placeholder(tf.float32)

    # model
    W = tf.Variable(tf.zeros([1]))
    b = tf.Variable(tf.zeros([1]))
    y = W * x + b

    # loss and train
    loss = tf.reduce_mean(tf.square(y_-y))
    optimizer = tf.train.GradientDescentOptimizer(0.0000001)
    train_step = optimizer.minimize(loss)

    # run session
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        for i in range(1000):
            xs = [i]
            ys = [3 * i]
            feed = {x: xs, y_: ys}
            sess.run(train_step, feed_dict=feed)
            if i % 100 == 0:
                print('iteration at %d:' % i)
                print('weight: %f' % sess.run(W))
                print('bias: %f' % sess.run(b))
                print('lost: %f' % sess.run(loss, feed_dict=feed))
# end linear_regression_01()


def linear_regression_02():
    # Create fake data for y = W.x + b where W = 2, b = actual_b
    datapoint_size = 1000
    actual_W = 2
    actual_b = 10

    all_xs = []
    all_ys = []
    for i in range(datapoint_size):
        x = i % 10
        all_xs.append(x)
        all_ys.append(actual_W*x+actual_b)

    all_xs = np.transpose([all_xs])
    all_ys = np.transpose([all_ys])

    # Model linear regression y = Wx + b
    x = tf.placeholder(tf.float32, [None, 1], name='x')
    y_ = tf.placeholder(tf.float32, [None, 1], name='y_')

    W = tf.Variable(tf.zeros([1, 1]), name='W')
    b = tf.Variable(tf.zeros([1]), name='b')
    with tf.name_scope('Wx_b') as scope:
        product = tf.matmul(x, W)
        y = product + b

    # Cost function sum((y_-y)**2)
    with tf.name_scope('cost') as scope:
        cost = tf.reduce_mean(tf.square(y_-y))
        cost_sum = tf.summary.scalar('cost', cost)

    # Training using Gradient Descent to minimize cost
    with tf.name_scope('train') as scope:
        learn_rate = 0.001
        train_step = tf.train.GradientDescentOptimizer(learn_rate).minimize(cost)

    # Add summary ops to collect data
    W_hist = tf.summary.histogram('weights', W)
    b_hist = tf.summary.histogram('biases', b)
    y_hist = tf.summary.histogram('y', y)
    # Merge all the summaries and write them out to /tmp/mnist_logs
    merged = tf.summary.merge_all()

    # Run session
    init = tf.initialize_all_variables()
    with tf.Session() as sess:
        sess.run(init)
        writer = tf.summary.FileWriter('./lr_summary', sess.graph)

        steps = 10000
        batch_size = 10
        for i in range(steps):
            # create mini batch of data
            batch_start_idx = (i * batch_size) % (datapoint_size - batch_size)
            batch_end_idx = batch_start_idx + batch_size
            batch_xs = all_xs[batch_start_idx:batch_end_idx]
            batch_ys = all_ys[batch_start_idx:batch_end_idx]
            xs = np.array(batch_xs)
            ys = np.array(batch_ys)

            feed = {x: xs, y_: ys}
            sess.run(train_step, feed_dict=feed)

            if i % 1000 == 0:
                # results: W should be close to actual_W, and b should be close to actual_b
                print('iteration at %d => W: %f, b: %f, cost: %f' %
                    (i, sess.run(W), sess.run(b), sess.run(cost, feed_dict=feed)))
                print('y: %s, y_: %s' % (sess.run(y, feed_dict=feed), ys))

            if i % 10 == 0:
                all_feed = {x: all_xs, y_: all_ys}
                summary = sess.run(merged, feed_dict=all_feed)
                writer.add_summary(summary, i)
    # end with
# end linear_regression_02()


if __name__ == '__main__':

    # linear_regression_01()
    linear_regression_02()

    print('tensorflow linear regression DONE!')
