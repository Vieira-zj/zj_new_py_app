# %%
import tensorflow as tf
import pandas as pd
pd.__version__, tf.__version__

# %%
# 前提：在pdms里面引入图片集
# from nbsdk import get_picture_data
# image_path = get_picture_data('mnist/123.image-set')
image_path = 'image_set_pdms_path'

# csv中每一行的数据有两列，[image] 图片的hdfs路径，[label] 图片对应的标注值
# 可以使用"tf.read_file(filepath)"的方式读取图片
df = pd.read_csv(image_path, delimiter=',', header=0)
df.columns, df.shape

# %%
image_data = df['image'].head(128).as_matrix().reshape(-1, 1)
label_data = df['label'].head(128).as_matrix().reshape(-1, 1)
image_data = image_data.reshape(-1)
label_data = label_data.reshape(-1)
image_data[:5], label_data[:5]

# %%
def _decode_image_file(filename, label):
    image_string = tf.read_file(filename)
    features = tf.image.decode_png(image_string)
    features = tf.image.resize_images(features, [28, 28])
    features = tf.cast(features, dtype=tf.float32)
    label = tf.one_hot(label, 10)
    return features, label

print('_decode_image_file')

# %%
image_list_placeholder = tf.placeholder(tf.string, [None])
label_list_placeholder = tf.placeholder(tf.int64, [None])

dataset = tf.data.Dataset.from_tensor_slices(
    (image_list_placeholder, label_list_placeholder))
dataset = dataset.repeat(1).map(
    _decode_image_file).batch(64).shuffle(buffer_size=1)
print('define tf dataset')

# %%
iterator = dataset.make_initializable_iterator()
batch_features_op, batch_label_op = iterator.get_next()
batch_features_op = tf.cast(batch_features_op, tf.float32)
batch_label_op = tf.cast(batch_label_op, tf.int64)
print('define iterator')

# %%
# 创建w参数
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

# 创建b参数
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

print('define weight and bais variable')

# %%
# 创建卷积层 步长为1, 周围补0, 输入与输出的数据大小一样（可得到补全的圈数）
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# 创建池化层 kernel大小为2, 步长为2, 周围补0, 输入与输出的数据大小一样（可得到补全的圈数）
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

print('define conv2d, max_pool_2x2')

# %%
# 第一层卷积 这里使用5*5的过滤器，因为是灰度图片，所以只有1个颜色通道，使用32个过滤器来建立卷积层
# 所以我们一共是有5*5*32个参数
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

# 数据加载出来以后是一个n*784的矩阵，每一行是一个样本。
# 784是灰度图片的所有的像素点。实际上应该是28*28的矩阵，平铺开之后的结果
# 但在cnn中我们需要把他还原成28*28的矩阵，所以要reshape
input_x_image = tf.reshape(batch_features_op, [-1, 28, 28])
x_image = tf.reshape(input_x_image, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
print('cnn layer 第一层卷积')

# %%
# 第二层卷积 同样使用5*5的过滤器，因为上一层使用32个过滤器所以相当于有32个颜色通道一样。而这一层我们使用64个过滤器
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)
print('cnn layer 第二层卷积')

# %%
# 全连接层 经过上面2层以后，图片大小变成了7*7
# 初始化权重，全连接层我们使用1024个神经元
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
# 铺平图像数据。因为这里不再是卷积计算了，需要把矩阵冲洗reshape成一个一维的向量
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])

# 全连接层计算
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# keep_prob表示保留不关闭的神经元的比例。为了避免过拟合，这里在全连接层使用dropout方法
# 就是随机地关闭掉一些神经元，使模型不要与原始数据拟合的那么准确
#keep_prob = tf.placeholder(tf.float32)
#h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
print('cnn layer 全连接层')

# %%
# 创建输出层
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.matmul(h_fc1, W_fc2) + b_fc2

softmax_op = tf.nn.softmax(y_conv)
prediction_op = tf.argmax(softmax_op, 1)

correct_prediction_op = tf.equal(prediction_op, batch_label_op)
accuracy_op = tf.reduce_mean(tf.cast(correct_prediction_op, tf.float32))
print('cnn layer 输出层')

# %%
# 训练过程
from tensorflow.python.saved_model import (
    signature_constants, signature_def_utils, utils)

# 1.计算交叉熵损失
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=batch_label_op, logits=y_conv))

# 2.创建优化器（注意这里用AdamOptimizer代替了梯度下降法）
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# 3.计算准确率
correct_prediction = tf.equal(
    tf.argmax(y_conv, 1), tf.argmax(batch_label_op, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# %%
with tf.Session() as sess:
    # 4.初始化所有变量
    sess.run(tf.global_variables_initializer())
    sess.run(iterator.initializer, feed_dict={
             image_list_placeholder: image_data, label_list_placeholder: label_data})

    while True:
      try:
        print('cnn training ...')
        sess.run(train_step)
      except tf.errors.OutOfRangeError:
        print('训练结束')
        break

    builder = tf.saved_model.builder.SavedModelBuilder(
        'cnn_model01/0')

    inputs = {'image': utils.build_tensor_info(input_x_image)}
    outputs = {
        'softmax': utils.build_tensor_info(softmax_op),
        'prediction': utils.build_tensor_info(prediction_op),
    }
    signature = tf.saved_model.signature_def_utils.build_signature_def(
        inputs, outputs, method_name=signature_constants.PREDICT_METHOD_NAME)
    builder.add_meta_graph_and_variables(
        sess, [tf.saved_model.tag_constants.SERVING],
        clear_devices=True,
        signature_def_map={
            tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
            signature}
    )
    builder.save()

print('tf session end')

# %%
# 保存模型到模型中心
# from nbsdk import export_model
# prn, hdfs = export_model('cnn_model01', 'cnn_model01')
# print(hdfs, prn)
print('cnn demo done')
