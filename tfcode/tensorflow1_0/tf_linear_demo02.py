# -*- coding: utf-8 -*-
'''
Created on 2019-05-19
@author: zhengjin

tensorflow board web:
$ tensorboard --logdir /tf/tf_scripts/summary
'''

import tensorflow as tf
import os


tf.app.flags.DEFINE_string('model_path', './linear_regression/', 'model save path.')
FLAGS = tf.app.flags.FLAGS


def linear_regression():
    with tf.variable_scope('original_data'):
        X = tf.random_normal(shape=(100, 1), mean=2, stddev=2, name='original_data_x')
        y_true = tf.matmul(X, [[0.8]], name='original_matmul') + 0.7

    with tf.variable_scope('linear_model'):
        weights = tf.Variable(initial_value=tf.random_normal(shape=(1, 1)), name='weights')
        bias = tf.Variable(initial_value=tf.random_normal(shape=(1, 1)), name='bias')
        y_predict = tf.matmul(X, weights, name='model_matmul') + bias

    with tf.variable_scope('loss'):
        loss = tf.reduce_mean(tf.square(y_predict - y_true), name='loss_op')

    with tf.variable_scope('gd_optimizer'):
        optimizer = tf.train.GradientDescentOptimizer(
            learning_rate=0.01, name='optimizer').minimize(loss)

    # 收集变量
    tf.summary.scalar('loss', loss)
    tf.summary.histogram('weights', weights)
    tf.summary.histogram('bias', bias)
    # 合并变量
    merge = tf.summary.merge_all()

    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(init)
        # 未经训练的权重和偏置
        print('random init weight: %f, bias: %f' % (weights.eval(), bias.eval()))

        # 当存在checkpoint文件，就加载模型
        if os.path.exists('./linear_regression/checkpoint'):
            saver.restore(sess, FLAGS.model_path)

        file_writer = tf.summary.FileWriter(logdir='./summary', graph=sess.graph)

        for i in range(100):
            sess.run(optimizer)
            print('at iter %i, loss: %f, weight: %f, bias: %f' %
                  (i, loss.eval(), weights.eval(), bias.eval()))
            summary = sess.run(merge)
            file_writer.add_summary(summary, i)
            if i % 10 == 0:
                saver.save(sess, FLAGS.model_path)

    if file_writer is not None:
        file_writer.close()


def main(argv):
    print('main func, and arguments:', argv)
    print('model save path:', FLAGS.model_path)
    linear_regression()


if __name__ == '__main__':

    tf.app.run()
    print('tensorflow linear regression DONE!')
