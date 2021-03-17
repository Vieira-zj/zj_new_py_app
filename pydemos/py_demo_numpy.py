# -*- coding: utf-8 -*-
'''
Created on 2019-05-26
@author: zhengjin

numpy 的核心是 ndarray 对象。
ndarray 的精髓在于 numpy 的两大特征：矢量化（vectorization）和广播（broadcast）。
矢量化可以理解为代码中没有显式的循环、索引等；广播可以理解为隐式地对每个元素实施操作。
'''

import numpy as np


def numpy_demo01():
    # create array
    arr1 = np.array([6, 7.5, 8, 0, 1])
    print('numpy 1d array:\n', arr1)
    print(type(arr1))
    for num in arr1:
        print(num)

    arr2 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    print('\nnumpy 2d array:\n', arr2)
    print('array: type=%r, len=%d, shape=%r' %
          (arr2.dtype, arr2.ndim, arr2.shape))

    print('\nzeros array:\n', np.zeros(10))
    print('ones array:\n', np.ones((3, 5)))
    print('array by range:\n', np.arange(10))


def numpy_demo02():
    # array dtype
    arr1 = np.array([1, 2, 3, 4], dtype=np.float64)
    arr2 = np.array([4, 3, 2, 1], dtype=np.int32)
    print('arr1 type: %r, arr2 type: %r' % (arr1.dtype, arr2.dtype))
    print('float array:\n', arr1)
    print('int array:\n', arr2)

    arr3 = arr2.astype(np.float32)
    print('arr3 type:', arr3.dtype)


def numpy_demo03():
    # operation on array
    arr = np.array([[1., 2., 3.], [4., 5., 6.]])
    print('arr * arr:\n', arr * arr)
    print('arr * 0.5:\n', arr * 0.5)


def numpy_demo04():
    # index and slice
    arr = np.arange(10)
    print('arr element at 5:', arr[5])
    print('arr element at 5~8:', arr[5:8])

    # 和list类型有很大的不同的是，操作原数组的子序列的时候，实际上就是操作原数组的数据
    arr_slice = arr[:4]
    arr_slice[:] = 10
    print('\narr slice:\n', arr_slice)
    print('src arr:\n', arr)

    # 复制操作
    arr_copy = arr[:3].copy()
    arr_copy[:] = 20
    print('\narr copy:\n', arr_copy)
    print('src arr:\n', arr)


def numpy_demo05():
    # index for 2d array
    arr2d = np.arange(1, 10).reshape((3, 3))
    print('2d [3,3] arr:\n', arr2d)

    print('arr 1st row:', arr2d[0])
    print('arr element at [0,1]:', arr2d[0][1])
    print('arr element at [1,1]:', arr2d[1, 1])

    arr2d[0] = 10
    print('update arr:\n', arr2d)


def numpy_demo06():
    # array function
    arr1 = np.arange(10)
    print('sqrt arr:\n', np.sqrt(arr1))
    print('square arr:\n', np.square(arr1))

    arr2 = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
    print('\nunique arr:\n', np.unique(arr2))

    arr3 = np.arange(32).reshape(8, 4)
    print('\nsum array:', arr3.sum())
    print('mean arr:', arr3.mean())
    print('mean for each row:\n', arr3.mean(axis=1))


def numpy_demo07():
    # create random array
    print('np.random.randint arr:\n', np.random.randint(1, 10, size=10))
    print('np.random.randint int64 value:',
          np.random.randint(1, 10, dtype=np.int64))
    print('np.random.randint 2d arr:\n', np.random.randint(1, 10, (3, 2)))

    # value=0.0~1.0
    print('\nnp.random.rand value:', np.random.rand())
    # shape=[3,2] value=0.0~1.0
    print('np.random.rand 2d arr:\n', np.random.rand(3, 2))
    print('np.random.random 2d arr:\n', np.random.random(size=(3, 2)))

    # value=0.0~1.0
    print('\nnp.random.uniform arr:\n', np.random.uniform(size=10))
    # shape=[3,2] value=1.0~10.0
    print('np.random.uniform 2d arr:\n',
          np.random.uniform(-1., 1., size=(3, 2)))

    # loc均值为1, scale标准差为3
    print('\nnp.random.normal arr:\n', np.random.normal(1, 3, size=10))
    print('np.random.normal 2d arr:\n', np.random.normal(0, 1, size=(3, 2)))

    f = np.random.uniform()
    print('float: %f, 2 decimal: %.2f' % (f, f))


def numpy_demo08():
    print('allclose 用于匹配两个数组')
    array1 = np.array([0.12, 0.17, 0.24, 0.29])
    array2 = np.array([0.13, 0.19, 0.26, 0.31])

    print(np.allclose(array1, array2, 0.1))  # 公差为0.1, False
    print(np.allclose(array1, array2, 0.2))  # 公差为0.2, True

    print('\nextract 根据特定条件从数组中提取元素')
    rand = np.random.RandomState(66)
    arr = rand.randint(20, size=12)
    print(arr)

    cond = np.mod(arr, 2) == 1
    print(np.extract(cond, arr))
    print(np.extract(((arr < 3) | (arr > 15)), arr))

    print('\nwhere 从满足特定条件的数组中返回元素的索引值')
    y = np.array([1, 5, 6, 8, 1, 7, 3, 6, 9])
    del cond
    cond = np.where(y > 5)
    print(cond)
    print(y[cond])

    print('\npercentile 计算沿指定轴的数组元素的第n个百分点')
    a = np.array([1, 5, 6, 8, 1, 7, 3, 6, 9])
    print(np.sort(a))
    print('50th Percentile of array, axis = 0:', np.percentile(a, 50, axis=0))

# -----------------------------------
# Part2
# -----------------------------------


def numpy_demo11():
    print('创建数组')
    print(np.array([1, 2, 3]))
    print(np.empty((2, 3)))
    print(np.zeros(2))
    print(np.ones(2))
    print(np.eye(3))


def numpy_demo12():
    print('创建随机数组')
    print(np.random.random(3))
    print(np.random.randint(2, size=10))
    print(np.random.randint(5, size=(2, 4)))
    print(np.random.randint(3, 10, (2, 4)))


def numpy_demo13():
    print('在数值范围内创建数组')
    print(np.arange(5))
    print(np.arange(0, 5, 2))
    print(np.linspace(0, 5, 5))
    print(np.linspace(0, 5, 5, endpoint=False))
    print(np.logspace(1, 3, 3))


def numpy_demo14():
    print('从已有数组创建数组')
    print(np.asarray([1, 2, 3]))
    print(np.empty_like(np.asarray([1, 2, 3])))
    print(np.zeros_like(np.asarray([1, 2, 3])))
    print(np.ones_like(np.asarray([1, 2, 3])))


def numpy_demo15():
    print('构造复杂数组')
    print('重复数组')
    a = np.arange(3)
    print(np.tile(a, 2))
    print(np.tile(a, (2, 3)))

    print('重复元素')
    print(a.repeat(2))


def numpy_demo16():
    print('切片和索引')
    a = np.arange(9)
    print(a)
    print(a[-1])  # 最后一个元素
    print(a[2:5])
    print(a[:7:3])  # 返回第0到第7个元素，步长为3
    print(a[::-1])  # 返回逆序的数组

    a = np.arange(24).reshape(2, 3, 4)  # 2层3行4列
    print(a)
    print(a[1, 2, 3])
    print(a[:, 0, 0])  # 所有楼层的第1排第1列


def numpy_demo17():
    print('改变数组的结构')
    a = np.array([[1, 2, 3], [4, 5, 6]])
    print(a.shape)
    print()
    print(a.reshape(3, 2))
    print(a)
    print(a.ravel())  # 返回一维数组
    print()
    a.resize((3, 2))  # 类似于reshape, 但会改变所操作的数组
    print(a)


def numpy_demo18():
    print('数组复制')
    a = np.arange(6).reshape((2, 3))
    b = a.view()  # 浅复制
    print(b)
    print(b is a)
    print(b.base is a)
    print(b.flags.owndata)

    print()
    c = a.copy()  # 深复制
    print(c)
    print(c is a)
    print(c.base is a)
    print(c.flags.owndata)


def numpy_demo19():
    print('数组合并')
    print('append')
    print(np.append([1, 2, 3], [[4, 5, 6], [7, 8, 9]]))
    print(np.append([[1, 2, 3]], [[4, 5, 6]], axis=0))
    print(np.append(np.array([[1, 2, 3]]), np.array([[4, 5, 6]]), axis=1))

    print('\nconcatenate')
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6]])
    print(np.concatenate((a, b), axis=0))
    print(np.concatenate((a, b.T), axis=1))
    print(np.concatenate((a, b), axis=None))


def numpy_demo20():
    print('数组拆分')
    a = np.arange(4).reshape(2, 2)
    print(a)
    x1, y1 = np.hsplit(a, 2)  # 水平拆分，返回list
    print(x1)
    print(y1)

    # x2, y2 = np.vsplit(a, 2)  # 垂直拆分，返回list
    # print(x2)
    # print(y2)


def numpy_demo21():
    print('数组排序')
    a = np.array([3, 1, 2])
    print(np.sort(a, kind='quicksort'))

    dt = np.dtype([('name', 'S10'), ('age', int)])
    a = np.array([('raju', 21), ('anil', 25),
                  ('ravi', 17), ('amar', 27)], dtype=dt)
    print(a)
    print(np.sort(a, order='name'))


def numpy_demo22():
    print('查找和筛选')
    a = np.array([0, 1, 0, 1, 2])
    print(np.nonzero(a))
    print()

    a = np.arange(10)
    print(np.where(a > 5))
    a = a.reshape((2, -1))
    print(np.where(a < 5))
    print()

    a = np.arange(12).reshape((3, 4))
    print(a)
    condition = np.mod(a, 3) == 0
    print(condition)
    print(np.extract(condition, a))


def numpy_demo23():
    print('增加元素')
    a = np.array([[1, 1], [2, 2], [3, 3]])
    print(a)

    print(np.insert(a, 1, 5))
    print(np.insert(a, 1, 5, axis=0))
    print(np.insert(a, 1, [5, 7], axis=0))
    print(np.insert(a, 1, 5, axis=1))


def numpy_demo24():
    print('减少元素')
    a = np.array([[1, 2], [3, 4], [5, 6]])
    print(a)

    print(np.delete(a, 1))
    print(np.delete(a, 1, axis=0))
    print(np.delete(a, 1, axis=1))


def numpy_demo25():
    print('去除重复元素')
    a = np.array([[1, 0, 0], [1, 0, 0], [2, 3, 4]])
    print(np.unique(a))
    print(np.unique(a, axis=0))
    print()

    u, indices = np.unique(a, return_index=True)
    print(u)
    print(indices)


def numpy_demo26():
    print('四舍五入')
    a = np.array([-0.42, -1.68, 0.37, 1.64])
    print(np.around(a))
    print(np.around(a, decimals=1))
    print()

    print('去尾')
    print(np.floor(a))
    print('进一')
    print(np.ceil(a))


if __name__ == '__main__':

    numpy_demo08()
    print('numpy demo DONE.')
