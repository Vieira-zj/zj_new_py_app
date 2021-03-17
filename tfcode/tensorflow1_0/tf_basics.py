# -*- coding: utf-8 -*-
'''
Created on 2019-05-18
@author: zhengjin
'''

import tensorflow as tf
import os


def tensorflow_variables():
    # defining variables
    weights = tf.Variable(tf.random_normal([2, 3], stddev=0.1), name='weights')
    print('weights name: %s, type: %s, shape: %s' %
          (weights.name, weights.dtype, weights.shape))

    biases = tf.Variable(tf.zeros([3]), name='biases')
    custom_var = tf.Variable(tf.zeros([3]), name='custom')

    # customized initializer
    custom_var_list = [weights, biases]
    init_custom_op = tf.variables_initializer(var_list=custom_var_list)

    # global initializer #1
    init_all_op = tf.global_variables_initializer()

    # global initializer #2
    # from tensorflow.python.framework import ops
    # all_variables_list = ops.get_collection(ops.GraphKeys.GLOBAL_VARIABLES)
    # init_all_op = tf.variables_initializer(var_list=all_variables_list)

    # initialization using other variables
    weights_new = tf.Variable(weights.initialized_value(), name='WeightsNew')
    init_weightsnew_op = tf.variables_initializer(var_list=[weights_new])

    # running the session
    is_custom = False
    with tf.Session() as sess:
        if is_custom:
            sess.run(init_custom_op)
        else:
            sess.run(init_all_op)
        sess.run(init_weightsnew_op)

        print('weights:', sess.run(weights))
        print('biases:', sess.run(biases))
        print('new weights:', sess.run(weights_new))


def tensorflow_scope():
    with tf.variable_scope('foo'):
        val = tf.get_variable('val', [1], initializer=tf.constant_initializer(1.0))
        print('val name:', val.name)

    # ValueError: Variable foo/v already exists, disallowed.
    # with tf.variable_scope('foo'):
    #     val = tf.get_variable('val', [1])

    # reuse=True
    with tf.variable_scope('foo', reuse=True):
        val_new = tf.get_variable('val', [1])
        print('val==val_new:', val == val_new)  # true


# tensorflow_flags
def main(argv):
    FLAGS = tf.app.flags.FLAGS
    print('string:', FLAGS.str_name)
    print('number:', FLAGS.int_name)
    print('bool:', FLAGS.bool_name)


if __name__ == '__main__':

    tf.app.flags.DEFINE_string('str_name', 'flag_str_val', 'flag string value test.')
    tf.app.flags.DEFINE_integer('int_name', 10, 'flag int value test.')
    tf.app.flags.DEFINE_boolean('bool_name', False, 'flag bool value test.')

    # tensorflow_variables()
    # tensorflow_scope()

    # run cmd:
    # python tensorflow_basics.py -h
    # python tensorflow_basics.py --str_name test_str --int_name 7 --bool_name True
    tf.app.run()  # run main function

    print('tensorflow basics DONE!')
