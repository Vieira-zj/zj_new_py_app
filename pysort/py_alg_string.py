# -*- coding: utf-8 -*-
'''
Created on 2020-05-28
@author: zhengjin
'''

import sys
import os
sys.path.append(os.getenv('PYPATH'))

from pysort import Stack

# -----------------------------------
# String
# -----------------------------------


def reverse_string(input_str: str) -> str:
    '''
    反转字符串
    '''
    start = 0
    end = len(input_str) - 1
    while start < end:
        input_str[start], input_str[end] = input_str[end], input_str[start]
        start += 1
        end -= 1
    return input_str


def is_recycle_string(input_str: str) -> bool:
    '''
    判断回文字符串
    '''
    start = 0
    end = len(input_str) - 1
    while start < end:
        if input_str[start] != input_str[end]:
            return False
        start += 1
        end -= 1
    return True


def test01():
    print('recycle string test:')
    for input_str in ['xyayx', 'ahha', 'haha']:
        print('%s is recycle string: %s' %
              (input_str, str(is_recycle_string(input_str))))


def get_longest_numbers(num_str: str) -> str:
    '''
    找出字符串中最长的连续数字
    '''
    start = cur_start = 0
    max_len = cur_len = 0

    for i in range(len(num_str) - 1):
        if num_str[i].isdigit():
            cur_len += 1
        else:
            cur_len = 0
            cur_start = i + 1

        if cur_len > max_len:
            max_len = cur_len
            start = cur_start
    return num_str[start:(start+max_len)]


def test02():
    num_str = 'abcd13579ed124ss123456789z'
    print('longest continuious numbers:', get_longest_numbers(num_str))


def filter_aba_string(aba_str: str) -> str:
    '''
    过滤掉输入字符串中的驼峰字符串（aba）
    input: AaabxbcdyayBxxy
    output: AaacdBxxy
    '''
    def is_aba_string(input_str):
        return input_str[0] == input_str[2]

    local_str = aba_str[:]
    i = 0
    while i < (len(local_str) - 2):
        if is_aba_string(local_str[i:i+3]):
            local_str = local_str[0:i] + local_str[i+3:]
        else:
            i += 1
    return local_str


def test03():
    aba_str = 'AaabxbcdyayBxxy'
    print('src aba string:', aba_str)
    print('filter aba string:', filter_aba_string(aba_str))


def str_distinct() -> list:
    '''
    有序字符串去重
    '''
    def format_line(in_str: str) -> str:
        return in_str.split('_')[0]

    f_path = os.path.join(os.getenv('PYPATH'), 'pysort/data/input.txt')
    with open(f_path, 'r') as in_f:
        lines = in_f.readlines()
        ret_list = [format_line(lines[0])]
        remove_list = []
        for i in range(1, len(lines)):
            line = format_line(lines[i])
            if ret_list[len(ret_list) - 1] != line:
                ret_list.append(line)
            else:
                remove_list.append(line)
        print('remove items:', ','.join(remove_list))
        return ret_list


def test05():
    print('distinct items:', ','.join(str_distinct()))


def str_ab_distinct(in_str: str) -> list:
    '''
    字符串去重 大写字母在小写字母前
    输入: EAAnCmCDffBg 输出: EACDBnmfg
    '''
    upper_chs = []
    lower_chs = []
    ret_list = []
    tmp_dict = {}

    for ch in in_str:
        if ch.isupper():
            upper_chs.append(ch)
            tmp_dict[ch] = 1
        if ch.islower():
            lower_chs.append(ch)
            tmp_dict[ch] = 1

    upper_chs.extend(lower_chs)
    for ch in upper_chs:
        if tmp_dict[ch] == 1:
            ret_list.append(ch)
            tmp_dict[ch] -= 1
    return ret_list


def str_ab_distinct02(in_str: str) -> list:
    upper_chs = []
    lower_chs = []
    tmp_dict = {}

    for ch in in_str:
        tmp_dict[ch] = tmp_dict.get(ch, 0) + 1
        if tmp_dict[ch] == 1:
            if ch.isupper():
                upper_chs.append(ch)
            else:
                lower_chs.append(ch)
    return upper_chs + lower_chs


def test06():
    input_str = 'EAAnCmCDffBg'
    ret1 = str_ab_distinct(input_str)
    print(''.join(ret1))
    ret2 = str_ab_distinct02(input_str)
    print(''.join(ret2))


# -----------------------------------
# Others
# -----------------------------------


def reverse_by_words(sentence: str) -> str:
    '''
    reverse words divied by space
    input: this is a test
    output: test a is this
    '''
    s = Stack()
    for word in sentence.split(' '):
        s.push(word)

    tmp_list = []
    while s.size() > 0:
        tmp_list.append(s.pop())
    return ' '.join(tmp_list)


def test04():
    sentence = 'this is a test'
    print('src text:', sentence)
    print('text reverse by words:', reverse_by_words(sentence))


if __name__ == '__main__':

    test06()
    print('py alg string demo done.')
