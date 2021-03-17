# -*- coding: utf-8 -*-
'''
Created on 2020-06-06
@author: zhengjin
'''


def int_to_binary(num: int, bin_dim: int) -> str:
    '''
    十进制整数转二进制
    '''
    bin_list = [str(b) for b in bin(num)[2:]]
    ret = ['0'] * (bin_dim - len(bin_list)) + bin_list
    return ''.join(ret)


def test01():
    num = 15
    bin_str = int_to_binary(num, 8)
    print('binary for %d is: %s' % (num, bin_str))


def binary_to_int(bits: list) -> int:
    '''
    二进制转十进制整数
    '''
    ret = 0
    for idx, bit in enumerate(reversed(bits)):
        ret += bit * pow(2, idx)
    return ret


def test02():
    bits = '00001111'
    num = binary_to_int([int(bit) for bit in bits])
    print('int for binary %s is: %d' % (bits, num))


if __name__ == '__main__':

    test02()
    print('py alg int demo done.')
