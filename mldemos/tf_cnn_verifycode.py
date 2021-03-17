'''
Created on 2020-06-09
@author: zhengjin
@desc: 利用 TF CNN 对验证码的数据集进行多分类
'''

import logging
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelBinarizer

# 日志设置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class TfCnn(object):

    def __init__(self, epoch, learning_rate, save_model_path):
        self.epoch = epoch  # 训练次数
        self.learning_rate = learning_rate
        self.save_model_path = save_model_path

        '''
        第一层 卷积层和池化层
        x_image(batch, 16, 20, 1) -> h_pool1(batch, 8, 10, 10)
        '''
        x = tf.placeholder(tf.float32, [None, 320])
        self.x = x
        x_image = tf.reshape(x, [-1, 16, 20, 1])
        W_conv1 = self.weight_variable([3, 3, 1, 10])
        b_conv1 = self.bias_variable([10])

        h_conv1 = tf.nn.relu(self.conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = self.max_pool_2x2(h_conv1)

        '''
        第二层 卷积层和池化层
        h_pool1(batch, 8, 10, 10) -> h_pool2(batch, 4, 5, 20)
        '''
        W_conv2 = self.weight_variable([3, 3, 10, 20])
        b_conv2 = self.bias_variable([20])

        h_conv2 = tf.nn.relu(self.conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = self.max_pool_2x2(h_conv2)

        '''
        第三层 全连接层
        h_pool2(batch, 4, 5, 20) -> h_fc1(1, 100)
        '''
        W_fc1 = self.weight_variable([4 * 5 * 20, 200])
        b_fc1 = self.bias_variable([200])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 4 * 5 * 20])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        '''
        第四层 Dropout层
        h_fc1 -> h_fc1_drop, 训练中启用, 测试中关闭
        '''
        self.keep_prob = tf.placeholder(dtype=tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

        '''
        第五层 Softmax输出层
        '''
        W_fc2 = self.weight_variable([200, 31])
        b_fc2 = self.bias_variable([31])
        self.y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

        '''
        训练和评估模型
        ADAM优化器来做梯度最速下降, feed_dict中加入参数keep_prob控制dropout比例
        '''
        self.y_true = tf.placeholder(shape=[None, 31], dtype=tf.float32)
        self.cross_entropy = - \
            tf.reduce_mean(tf.reduce_sum(
                self.y_true * tf.log(self.y_conv), axis=1))  # 计算交叉熵

        # 使用adam优化器来以0.0001的学习率来进行微调
        self.train_model = tf.train.AdamOptimizer(
            self.learning_rate).minimize(self.cross_entropy)

        self.saver = tf.train.Saver()
        logger.info('Initialize the model...')

    def train(self, x_data, y_data):
        logger.info('Training the model...')

        with tf.Session() as sess:
            # 对所有变量进行初始化
            sess.run(tf.global_variables_initializer())

            feed_dict = {self.x: x_data,
                         self.y_true: y_data, self.keep_prob: 1.0}
            # 进行迭代学习
            for i in range(self.epoch + 1):
                sess.run(self.train_model, feed_dict=feed_dict)
                if i % int(self.epoch / 50) == 0:
                    print('已训练%d次, loss: %s.' %
                          (i, sess.run(self.cross_entropy, feed_dict=feed_dict)))

            # 保存CNN模型
            logger.info('Saving the model...')
            self.saver.save(sess, self.save_model_path)

    def predict(self, data):
        with tf.Session() as sess:
            logger.info('Restoring the model...')
            self.saver.restore(sess, self.save_model_path)
            predict = sess.run(self.y_conv, feed_dict={
                               self.x: data, self.keep_prob: 1.0})

        return predict

    '''
    权重初始化
    初始化为一个接近0的很小的正数
    '''

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    '''
    卷积和池化，使用卷积步长为1（stride size）, 0边距（padding size）
    池化用简单传统的2x2大小的模板做max pooling
    '''

    def conv2d(self, x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(self, x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def train_main():
    csv_file_path = 'data/verifycode.csv'
    df = pd.read_csv(csv_file_path)

    # 数据集的特征
    features = ['v'+str(i+1) for i in range(16*20)]
    labels = df['label'].unique()

    # 对样本的真实标签进行标签二值化
    lb = LabelBinarizer()
    lb.fit(labels)
    y_ture = pd.DataFrame(lb.transform(df['label']), columns=[
                          'y'+str(i) for i in range(31)])
    y_bin_columns = list(y_ture.columns)

    for col in y_bin_columns:
        df[col] = y_ture[col]

    # 将数据集分为训练集和测试集, 训练集70%, 测试集30%
    x_train, x_test, y_train, y_test = train_test_split(
        df[features], df[y_bin_columns], train_size=0.7, test_size=0.3, random_state=123)

    # 使用CNN进行预测
    model_save_path = '/tmp/test/cnn_verifycode.ckpt'
    cnn = TfCnn(1000, 0.0005, model_save_path)

    # 训练CNN
    cnn.train(x_train, y_train)

    # 预测数据
    y_pred = cnn.predict(x_test)
    # 预测分类
    label = '123456789ABCDEFGHJKLNPQRSTUVXYZ'
    prediction = []
    for pred in y_pred:
        label = labels[list(pred).index(max(pred))]
        prediction.append(label)

    # 计算预测的准确率
    x_test['prediction'] = prediction
    x_test['label'] = df['label'][y_test.index]
    print(x_test.head())
    accuracy = accuracy_score(x_test['prediction'], x_test['label'])
    print('CNN的预测准确率为%.2f%%.' % (accuracy*100))


if __name__ == '__main__':

    train_main()
    print('tf cnn verifycode demo done.')
