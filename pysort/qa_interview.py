# -*- coding: utf-8 -*-
'''
Created on 2020-07-03
@author: zhengjin
'''

import random
import time


def alg_demo01(input: list) -> list:
    '''
    shuffle算法：每次从未处理的数据中随机取出一个数字，然后把该数字放在数组的尾部，即数组尾部存放的是已经处理过的数字。
    注：原始数据被直接打乱。
    '''
    for i in range((len(input) - 1), 0, -1):
        idx = random.randint(0, i)
        input[i], input[idx] = input[idx], input[i]


def test_alg_demo01():
    input = [i for i in range(0, 10)]
    print('src list:', input)
    alg_demo01(input)
    print('shuffled list:', input)


def alg_demo02(num: int) -> int:
    '''
    某商店规定：3个空汽水瓶可以换1瓶汽水。小张手上有10个空汽水瓶，她最多可以换多少瓶汽水喝？答案是5瓶。
    先用9个空瓶子换3瓶汽水，喝掉3瓶满的，喝完以后4个空瓶子；
    用3个再换1瓶，喝掉这瓶满的，这时候剩2个空瓶子；
    然后你让老板先借给你1瓶汽水，喝掉这瓶满的，喝完以后用3个空瓶子换1瓶满的还给老板。
    如果小张手上有n个空汽水瓶，最多可以换多少瓶汽水喝？
    '''
    if num < 2:
        return 0
    elif num == 2:
        return 1

    ret_num = int(num / 3)
    remained1 = num % 3
    remained2 = ret_num
    ret_num += alg_demo01(remained1 + remained2)
    return ret_num


def test_alg_demo02():
    inputs = (2, 10, 100)
    expected_res = (1, 5, 50)
    for num, expected in zip(inputs, expected_res):
        ret = alg_demo02(num)
        print('%d => %d' % (num, ret))
        assert(ret == expected)


class FindCoder(object):
    '''
    再给定的字符串数组中，找到包含"Coder"的字符串（不区分大小写），并将其作为一个新的数组返回。
    结果字符串的顺序按照"Coder"出现的次数递减排列，若两个串中"Coder"出现的次数相同，则保持他们在原数组中的位置关系。

    给定一个字符串数组A和它的大小n, 请返回结果数组。
    保证原数组大小小于等于300, 其中每个串的长度小于等于200. 同时保证一定存在包含coder的字符串。

    输入：["i am a coder","Coder Coder","Code"]
    返回：["Coder Coder","i am a coder"]
    '''

    def find(self, input_list_of_str: list) -> list:
        tmp_list_of_dict = []
        for s in input_list_of_str:
            tmp_list_of_dict.append(self.findWords(s))
        tmp_list_of_dict = [d for d in tmp_list_of_dict if d['length'] > 0]

        ret_list = []
        for d in tmp_list_of_dict:
            self.insertWithOrder(ret_list, d)
        return [item['text'] for item in ret_list]

    def findWords(self, input: str) -> list:
        words = input.split(' ')
        words_list = [word for word in words if word.lower() == 'coder']
        return {'text': input, 'length': len(words_list)}

    def insertWithOrder(self, input_list: list, item_dict: dict):
        for i in range(len(input_list)):
            if input_list[i]['length'] < item_dict['length']:
                input_list.insert(i, item_dict)
                return
            elif input_list[i]['length'] == item_dict['length']:
                if (i+1) < len(input_list):
                    input_list.insert(i+1, item_dict)
                else:
                    input_list.append(item_dict)
                return
        input_list.append(item_dict)


def test_find_coder():
    input = ['i am a coder', 'Coder Coder', 'Code', 'more coder']
    fc = FindCoder()
    print(fc.find(input))


def alg_demo0401(input_list: list) -> list:
    '''
    请设计程序使连续的整数序列取前后两个数，并输出所有的列表。
    输入: [3,2,7,8,1,4,10,11,12,14]
    输出: [1,4],[7,8],[10,12],[14]
    '''
    ret_list = []
    sort_list = sorted(input_list)

    start = 0
    for i in range(len(sort_list) - 1):
        if (sort_list[i + 1] - sort_list[i]) != 1:
            if sort_list[start] == sort_list[i]:
                ret_list.append([sort_list[start]])
            else:
                ret_list.append([sort_list[start], sort_list[i]])
            start = i + 1

    if start == (len(sort_list) - 1):
        ret_list.append([sort_list[start]])
    else:
        ret_list.append([sort_list[start], sort_list[len(sort_list) - 1]])
    return ret_list


def alg_demo0402(input_list: list) -> list:
    ret_list = []
    sort_list = sorted(input_list)

    start = end = 0
    while end < (len(sort_list) - 1):
        if sort_list[end + 1] - sort_list[end] == 1:
            end += 1
            continue
        if start == end:
            ret_list.append([sort_list[start]])
        else:
            ret_list.append([sort_list[start], sort_list[end]])
        start = end = end + 1

    if start == end:
        ret_list.append([sort_list[start]])
    else:
        ret_list.append([sort_list[start], sort_list[end]])
    return ret_list


def test_alg_demo04():
    l = [3, 2, 7, 8, 1, 4, 10, 17, 11, 12, 14]
    print(alg_demo0401(l))
    print(alg_demo0402(l))


def alg_demo05(in_str: str) -> str:
    '''
    从一个字符串中找出出现频率最高且最先出现的字符。
    '''
    d_count = {}
    d_pos = {}
    res_chs = []
    max_cnt = 0
    for i in range(len(in_str)):
        ch = in_str[i]
        if not ch in d_pos.keys():
            d_pos[ch] = i
        cnt = d_count.get(ch, 0) + 1
        d_count[ch] = cnt
        if cnt > max_cnt:
            max_cnt = cnt
            res_chs = [ch]
        elif cnt == max_cnt:
            res_chs.append(ch)

    ret_ch = res_chs[0]
    if len(res_chs) == 1:
        return ret_ch

    min_pos = d_pos[ret_ch]
    for ch in res_chs[1:]:
        if d_pos[ch] < min_pos:
            ret_ch = ch
    return ret_ch


def test_alg_demo05():
    for in_str in ('mnq', 'cadxybazb', 'bcbdyxymny'):
        print(alg_demo05(in_str))


def alg_demo06(aba_str: str) -> str:
    '''
    过滤掉输入字符串中的驼峰字符串（aba）。
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


def test_alg_demo06():
    aba_str = 'AaabxbcdyayBxxy'
    print('src aba string:', aba_str)
    print('filter aba string:', alg_demo06(aba_str))


def alg_demo07(x: str, y: str) -> str:
    """
    考虑 x, y 转换成 int 时可能会超过整型最长大度，导致溢出的情况，因此每位数分别进行计算。
    fix: 只能处理两个正整数相加的情况。
    """
    x = reversed(x)
    x_nums = []
    for num in x:
        x_nums.append(int(num))
    y = reversed(y)
    y_nums = []
    for num in y:
        y_nums.append(int(num))

    # 补0 位数对齐
    append_size = abs(len(y_nums) - len(x_nums))
    if len(x_nums) < len(y_nums):
        x_nums.extend([0 for i in range(append_size)])
    else:
        y_nums.extend([0 for i in range(append_size)])
    # 最后可能进一位的情况
    x_nums.append(0)
    y_nums.append(0)

    # 计算
    res = []
    more = 0
    for i in range(len(x_nums)):
        tmp = more if more > 0 else 0
        tmp += x_nums[i] + y_nums[i]
        if tmp >= 10:
            more = 1
            res.append(tmp - 10)
        else:
            more = 0
            res.append(tmp)

    res = [str(item) for item in res]
    res = ''.join(reversed(res))
    return res[1:] if res.startswith('0') else res


def test_alg_demo07():
    for x, y in ((12345678, 9812743), (9999, 5741)):
        print('expect:', x+y)
        res = alg_demo07(str(x), str(y))
        print('actual', res)


def test_alg_demo08():
    """
    Write a decorator to find slow functions (execution time greater than 600ms).
    """
    def profile(fn):
        def wrap(*args):
            start = time.time()
            fn(*args)
            end = time.time()
            duration = round((end - start) * 1000)
            # print(duration)
            if duration > 600:
                print('slow func:', fn.__name__)
        return wrap

    @profile
    def run1():
        time.sleep(0.5)

    @profile
    def run2():
        time.sleep(1)

    @profile
    def run3():
        time.sleep(0.2)

    @profile
    def run4(text):
        print(text)
        time.sleep(0.7)

    for run in (run1, run2, run3):
        run()
    run4('hello')


def alg_demo09(text: str) -> str:
    """
    找出连续的字符串。
    input: abdechjk output: abcde
    input: abbacefhdj output: abcdef
    """
    ch_to_int = {}
    for idx, ch in enumerate('abcdefghijklmn'):
        ch_to_int[ch] = idx

    from functools import cmp_to_key

    def my_cmp(a, b):
        return ch_to_int[a] - ch_to_int[b]

    chs = [ch for ch in text]
    sorted_chs = sorted(chs, key=cmp_to_key(my_cmp))

    res_list = []
    for i in range(len(sorted_chs) - 1):
        ch = sorted_chs[i]
        next_ch = sorted_chs[i+1]
        if ch_to_int[next_ch] - ch_to_int[ch] == 0:
            continue
        res_list.append(ch)
        if ch_to_int[next_ch] - ch_to_int[ch] > 1:
            break
    return ''.join(res_list)


def test_alg_demo09():
    test_data = (('abdechjk', 'abcde'), ('abbacefhdj', 'abcdef'))
    for data, want in test_data:
        got = alg_demo09(data)
        print(got)
        assert got == want, f'want {want}, got {got}'


if __name__ == '__main__':

    test_alg_demo09()
    print('py alg interview demo done.')
