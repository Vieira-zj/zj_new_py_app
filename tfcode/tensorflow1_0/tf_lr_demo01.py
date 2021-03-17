# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin
'''

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('/tmp/data/', one_hot=True)
print('data count:', mnist.train.num_examples)  # 55000


def tf_logistic_regression():
    # tf Graph Input
    # mnist data image of shape 28*28=784
    x = tf.placeholder(tf.float32, [None, 784])
    # 0-9 digits recognition => 10 classes
    y = tf.placeholder(tf.float32, [None, 10])

    # Set model weights
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    # Construct model
    pred = tf.nn.softmax(tf.matmul(x, W) + b)  # Softmax
    print('predict shape:', pred.shape)  # [*, 10]

    # Minimize error using cross entropy
    cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
    # Gradient Descent
    learning_rate = 0.01
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    # Initialize the variables
    init = tf.global_variables_initializer()
    # Start training
    with tf.Session() as sess:
        # Run the initializer
        sess.run(init)

        # Training cycle
        training_epochs = 25
        batch_size = 100
        display_step = 1
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(mnist.train.num_examples/batch_size)

            # Loop over all batches
            for i in range(total_batch):
                batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                feed_dict = {x: batch_xs, y: batch_ys}
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost], feed_dict=feed_dict)
                # Compute average loss
                avg_cost += c / total_batch

            # Display logs per epoch step
            if (epoch+1) % display_step == 0:
                print('Epoch:', '%04d' % (epoch+1), 'cost =', '{:.9f}'.format(avg_cost))
        # end for

        print('Optimization Finished')
        print('acutal y:', sess.run(pred, feed_dict=feed_dict)[0])  # shape=[100,10]
        print('label y:', sess.run(y, feed_dict=feed_dict)[0])  # shape=[100,10]

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print('Accuracy:', accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
    # end with

# tf_logistic_regression output:
# ...
# Epoch: 0023 cost= 0.337950009
# Epoch: 0024 cost= 0.335731350
# Epoch: 0025 cost= 0.333707804
# Optimization Finished!


if __name__ == '__main__':

    tf_logistic_regression()
    print('tensorflow logistic expression DONE!')
