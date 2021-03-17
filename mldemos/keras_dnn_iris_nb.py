# %%
import os
import numpy as np
import tensorflow.keras as keras
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.__version__, keras.__version__

# %%
print('init')
np.random.seed(6)
tf.random.set_seed(13)

# %%
# STEP1: 读取CSV数据集, 并拆分为训练集和测试集
print('Iris dataset using Keras/TensorFlow')
IRIS = pd.read_csv('data/iris.csv')
target_var = 'class'  # 目标变量
IRIS.shape

# %%
features = list(IRIS.columns)
features.remove(target_var)
features

# %%
# 目标变量的类别
Class = IRIS[target_var].unique()
# 目标变量的类别字典
Class_dict = dict(zip(Class, range(len(Class))))
print(Class_dict)

# 增加一列target, 将目标变量进行编码
IRIS['target'] = IRIS[target_var].apply(lambda x: Class_dict[x])
IRIS['target'][:5]

# %%
# 对目标变量进行0-1编码（One-hot Encoding）
lb = LabelBinarizer()
lb.fit(list(Class_dict.values()))
transformed_labels = lb.transform(IRIS['target'])
transformed_labels.shape

# %%
y_bin_labels = []  # 对多分类进行0-1编码的变量
for i in range(transformed_labels.shape[1]):
    y_bin_labels.append('y' + str(i))
    IRIS['y' + str(i)] = transformed_labels[:, i]

IRIS.shape, IRIS.columns

# %%
# 将数据集分为训练集和测试集
train_x, test_x, train_y, test_y = train_test_split(
    IRIS[features], IRIS[y_bin_labels], train_size=0.7, test_size=0.3, random_state=0)

train_x.shape, train_y.shape

# %%
# STEP2: 定义模型
init = keras.initializers.glorot_uniform(seed=1)
simple_adam = keras.optimizers.Adam()

model = keras.Sequential()
model.add(keras.layers.Dense(units=5, input_dim=4,
                             kernel_initializer=init, activation='relu'))
model.add(keras.layers.Dense(
    units=6, kernel_initializer=init, activation='relu'))
model.add(keras.layers.Dense(
    units=3, kernel_initializer=init, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer=simple_adam, metrics=['accuracy'])

model.summary()

# %%
# STEP3: 训练模型
b_size = 1
max_epochs = 100
print('Starting training')
h = model.fit(train_x, train_y, batch_size=b_size,
              epochs=max_epochs, shuffle=True, verbose=1)
print('Training finished')

# %%
# STEP4: 评估模型
eval = model.evaluate(test_x, test_y, verbose=0)
print('Evaluation on test data: loss = %0.6f accuracy = %0.2f%%' %
      (eval[0], eval[1] * 100))

# %%
print('Saving model to disk')
model_path = '/tmp/test/testiris_model.h5'
model.save(model_path)

# %%
# STEP5: 使用模型进行预测
is_load_model = True
if is_load_model:
    print('Using loaded model to predict')
    model = keras.models.load_model(model_path)
    model.summary()

# %%
np.set_printoptions(precision=4)
unknown = np.array([[6.1, 3.1, 5.1, 1.1]], dtype=np.float32)
predicted = model.predict(unknown)
print('Using model to predict species for features:')
print(unknown)
print('Predicted softmax vector is:')
print(predicted)
np.argmax(predicted)

# %%
species_dict = {v: k for k, v in Class_dict.items()}
print('Predicted species is:', species_dict[np.argmax(predicted)])

# %%
# 补充
# np array
dim = np.arange(9).reshape(3, 3)
dim

# %%
# row=0,col=1 => point: x=1,y=0
print(dim[0][1])
# row=1,col=0 => point: x=0,y=1
print(dim[1][0])

print(dim[0, 1])
print(dim[1, 0])

print(dim[1, :])
print(dim[:2, :])

# %%
# pd dataframe
ser1 = pd.Series(np.arange(1, 10))
ser2 = pd.Series(np.arange(11, 20))
df = pd.DataFrame({'col1': ser1, 'col2': ser2})
df

# %%
print(df.iloc[0, 1])
print(df.iloc[1, 0])

print(df.loc[0, 'col1'])
print(df.loc[1, 'col2'])

print(df.iloc[:5, 0])
print(df.loc[:5, 'col1'])
print(df.loc[:5, :])

# %%
print('keras dnn iris demo done.')
