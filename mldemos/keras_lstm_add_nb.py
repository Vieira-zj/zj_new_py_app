# %%
# LSTM模型在实现整数加法运算
import numpy as np
import tensorflow.keras as keras

np.__version__, keras.__version__
# 0-255 间的加法, 8位二进制
BINARY_DIM = 8

# %%
def int_2_binary(number, binary_dim) -> list:
    '''
    将整数表示成为binary_dim位的二进制数, 高位用0补齐
    '''
    binary_list = list(map(lambda x: int(x), bin(number)[2:]))
    number_dim = len(binary_list)
    result_list = [0] * (binary_dim - number_dim) + binary_list
    return result_list

int_2_binary(10, BINARY_DIM)

# %%
def binary2int(binary_array) -> int:
    '''
    将一个二进制数组转为整数
    '''
    ret = 0
    for idx, val in enumerate(reversed(binary_array)):
        ret += val * pow(2, idx)
    return ret

binary2int([1, 0, 1, 0])

# %%
# 将 [0,2**BINARY_DIM) 所有数表示成二进制
binary = np.array([int_2_binary(i, BINARY_DIM)
                   for i in range(pow(2, BINARY_DIM))])
print(binary.shape)
binary[10, :]

# %%
# 样本的输入向量和输出向量
dataX = []
dataY = []
for i in range(binary.shape[0]):
    for j in range(binary.shape[0]):
        dataX.append(np.append(binary[i], binary[j]))
        dataY.append(int_2_binary(i + j, BINARY_DIM+1))

print(len(dataX), dataX[0].shape, len(dataY))
dataX[10], dataY[10]

# %%
# 特征X和目标变量Y数组, 适应LSTM模型的输入和输出
X = np.reshape(dataX, (len(dataX), 2*BINARY_DIM, 1))
Y = np.array(dataY)
print(X.shape, Y.shape)
X[10], Y[10]

# %%
# 定义LSTM模型
model = keras.models.Sequential()
model.add(keras.layers.LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.Dense(Y.shape[1], activation='sigmoid'))
model.compile(loss=keras.losses.mean_squared_error, optimizer='adam')

model.summary()

# %%
# plot model
# keras.utils.plot_model(model, to_file='/tmp/model.png', show_shapes=True)

# 模型训练（全量）
epochs = 20
model.fit(X, Y, epochs=epochs, batch_size=128)
# 保存模型
save_path = '/tmp/test/LSTM_Operation.h5'
model.save(save_path)

print('train and save model.')

# %%
# LSTM模型预测
for _ in range(20):
    start = np.random.randint(0, len(dataX) - 1)
    number1 = dataX[start][0:BINARY_DIM]
    number2 = dataX[start][BINARY_DIM:]

    correct = 0
    print('='*30)
    print('%s: %s' % (number1, binary2int(number1)))
    print('%s: %s' % (number2, binary2int(number2)))

    # X[start].shape = (16, 1)
    sample = np.reshape(X[start], (1, 2*BINARY_DIM, 1))
    predict = np.round(model.predict(sample), 0).astype(np.int32)[0]
    print('%s: %s' % (predict, binary2int(predict)))

print('LSTM predict done.')

# %%
print('keras LSTM add demo done.')
