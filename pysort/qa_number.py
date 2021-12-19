# -*- coding: utf-8 -*-
'''
Created on 2020-06-06
@author: zhengjin
'''


def int_to_binary_v1(num: int) -> int:
    count = 0
    ret = ''
    while num > 0:
        tmp = num % 2
        if tmp == 1:
            count += 1
        ret = str(tmp) + ret
        num = int(num / 2)
    print('binary:', ret)
    return count


def test_int_to_binary_v1():
    for num in (1, 2, 8, 9):
        print(int_to_binary_v1(num))


def int_to_binary_v2(num: int, bin_dim: int) -> str:
    '''
    十进制整数转二进制。
    '''
    bin_list = [str(b) for b in bin(num)[2:]]
    ret = ['0'] * (bin_dim - len(bin_list)) + bin_list
    return ''.join(ret)


def test_int_to_binary_v2():
    num = 15
    bin_str = int_to_binary_v2(num, 8)
    print('binary for %d is: %s' % (num, bin_str))


def binary_to_int(bits: list) -> int:
    '''
    二进制转十进制整数。
    '''
    ret = 0
    for idx, bit in enumerate(reversed(bits)):
        ret += bit * pow(2, idx)
    return ret


def test_binary_to_int():
    bits = '00001111'
    num = binary_to_int([int(bit) for bit in bits])
    print('int for binary %s is: %d' % (bits, num))


if __name__ == '__main__':

    test_int_to_binary_v1()
    print('py alg number demo done.')
