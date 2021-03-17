# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin
'''

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


def tf_neural_network_raw():
    # Network Parameters
    num_input = 784  # MNIST data input (img shape: 28*28)
    num_classes = 10  # MNIST total classes (0-9 digits)
    n_hidden_1 = 256  # 1st layer number of neurons
    n_hidden_2 = 256  # 2nd layer number of neurons

    # tf Graph input
    X = tf.placeholder('float', [None, num_input])
    Y = tf.placeholder('float', [None, num_classes])

    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_hidden_2, num_classes]))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([num_classes]))
    }

    # Create model
    def neural_net(x):
        # Hidden fully connected layer with 256 neurons, layer_1.shape=[?, 256]
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        # Hidden fully connected layer with 256 neurons, layer_2.shape=[?, 256]
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # Output fully connected layer with a neuron for each class, out_layer=[?, 10]
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return out_layer

    # Construct model
    logits = neural_net(X)
    prediction = tf.nn.softmax(logits)

    # Define loss and optimizer
    learning_rate = 0.1
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()
    # Start training
    with tf.Session() as sess:
        sess.run(init)

        num_steps = 500
        batch_size = 128
        display_step = 100
        for step in range(1, num_steps+1):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            feed_dict = {X: batch_x, Y: batch_y}
            # Run optimization op
            sess.run(train_op, feed_dict=feed_dict)

            if step % display_step == 0 or step == 1:
                # Calculate batch loss and accuracy
                loss, acc = sess.run([loss_op, accuracy], feed_dict=feed_dict)
                print('Step ' + str(step) + ', Minibatch Loss= ' + '{:.4f}'.format(loss) +
                      ', Training Accuracy= ' + '{:.3f}'.format(acc))
        # end for

        print('Optimization Finished')
        # Calculate accuracy for MNIST test images
        print('Testing Accuracy:', sess.run(
            accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels}))

# tf_neural_network_raw output:
# Step 1, Minibatch Loss= 5811.0991, Training Accuracy= 0.391
# Step 100, Minibatch Loss= 501.8816, Training Accuracy= 0.844
# Step 200, Minibatch Loss= 166.9854, Training Accuracy= 0.898
# Step 300, Minibatch Loss= 58.1946, Training Accuracy= 0.914
# Step 400, Minibatch Loss= 60.9300, Training Accuracy= 0.891
# Step 500, Minibatch Loss= 29.9656, Training Accuracy= 0.898
# Optimization Finished
# Testing Accuracy: 0.8687


if __name__ == '__main__':

    tf_neural_network_raw()
    print('tensorflow neural network DONE!')
