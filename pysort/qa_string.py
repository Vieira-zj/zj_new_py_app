# -*- coding: utf-8 -*-
'''
Created on 2020-05-28
@author: zhengjin
'''

import sys
import os
from typing import List

sys.path.append(os.getenv('PYPROJECT'))
from pysort import Stack

# -----------------------------------
# String
# -----------------------------------


def find_substring(src_str: str, sub_str: str) -> int:
    """
    查找子字符串，并返回下标。
    """
    if len(src_str) < len(sub_str):
        return -1
    if len(src_str) == 0 or len(sub_str) == 0:
        return -1

    for i in range(0, len(src_str) - len(sub_str) + 1):
        isFound = True
        for j in range(0, len(sub_str)):
            if src_str[i+j] != sub_str[j]:
                isFound = False
                break
        if isFound:
            return i
    return -1


def test_find_substring():
    for src_str, sub_str in [('abcd', 'ab'), ('abcd', 'bc'), ('abcd', 'cd'), ('abcd', 'cx'), ('ab', 'ab')]:
        print(find_substring(src_str, sub_str))


def reverse_string(src_str: str) -> str:
    """
    反转字符串。
    """
    chs = [ch for ch in src_str]
    start = 0
    end = len(chs) - 1
    while start < end:
        chs[start], chs[end] = chs[end], chs[start]
        start += 1
        end -= 1
    return ''.join(chs)


def test_reverse_string():
    for item in ('abcd', 'abcde'):
        print(reverse_string(item))


def is_recycle_string(input_str: str) -> bool:
    """
    判断回文字符串。
    """
    start = 0
    end = len(input_str) - 1
    while start < end:
        if input_str[start] != input_str[end]:
            return False
        start += 1
        end -= 1
    return True


def test_is_recycle_string():
    for input_str in ['xyayx', 'ahha', 'haha']:
        res = is_recycle_string(input_str)
        print('%s is recycle string: %s' % (input_str, res))


def get_longest_numbers(num_str: str) -> str:
    """
    找出字符串中最长的连续数字。
    """
    start = 0
    max_len = cur_len = 0
    for idx in range(0, len(num_str)):
        if num_str[idx].isdigit():
            cur_len += 1
            continue
        if cur_len > max_len:
            max_len = cur_len
            start = idx - cur_len
        cur_len = 0

    return num_str[start:(start+max_len)]


def test_get_longest_numbers():
    num_str = 'abcd13579ed124ss123456789z'
    print('longest continuious numbers:', get_longest_numbers(num_str))


def str_distinct() -> list:
    """
    有序字符串去重。
    """
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


def test_str_distinct():
    print('distinct items:', ','.join(str_distinct()))


def str_ab_distinct(in_str: str) -> list:
    """
    字符串去重，并且大写字母在小写字母前。
    输入: EAAnCmCDffBg 输出: EACDBnmfg
    """
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


def test_str_ab_distinct():
    input_str = 'EAAnCmCDffBg'
    ret1 = str_ab_distinct(input_str)
    print(''.join(ret1))
    ret2 = str_ab_distinct02(input_str)
    print(''.join(ret2))


def longest_common_prefix(strs: List[str]) -> str:
    if not strs:
        return ""
    if len(strs) == 0:
        return ""
    if len(strs) == 1:
        return strs[0]

    minStr = strs[0]
    for s in strs[1:]:
        if len(s) < len(minStr):
            minStr = s

    for i in range(len(minStr), 0, -1):
        sub = minStr[:i]
        matched = True
        for s in strs:
            if not s.startswith(sub):
                matched = False
                break
        if matched:
            return sub
    return ""


def longest_common_prefix02(strs: List[str]) -> str:
    # str[闭区间:开区间]
    if not strs:
        return ""
    if len(strs) == 0:
        return ""
    if len(strs) == 1:
        return strs[0]

    prefix = strs[0]
    for s in strs[1:]:
        if len(s) < len(prefix):
            prefix = s

    for s in strs:
        while len(prefix) > 0 and (not s.startswith(prefix)):
            prefix = prefix[:-1]
        if len(prefix) == 0:
            return ''
    return prefix


def test_longest_common_prefix():
    data = (
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        (['ab', 'a'], 'a'),
        ([], ''),
    )
    for value, expect in data:
        actual = longest_common_prefix02(value)
        assert actual == expect, f'{input} failed, expect={expect}, atucal={actual}'
        print(actual if len(actual) > 0 else 'null')


def length_of_longest_unique_substring(input: str) -> int:
    """
    无重复字符的最长子串。

    输入: "abcabcbb" 输出: 3
    输入: "bbbbb" 输出: 1
    输入: "pwwkew" 输出: 3
    """
    ret = 0
    i = j = 0
    while i < len(input):
        sub = {}
        while j < len(input):
            ch = input[j]
            if ch in sub.keys():
                break
            sub[ch] = None
            j += 1
        if len(sub) > ret:
            print(sub.keys())
            ret = len(sub)
        i = j

    return ret


def test_length_of_longest_unique_substring():
    for value, want in (('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3)):
        got = length_of_longest_unique_substring(value)
        print(f'{value} got: {got}')
        assert got == want, f'got: {got}, want: {want}'


# -----------------------------------
# Others
# -----------------------------------

def reverse_by_words(sentence: str) -> str:
    """
    reverse words divied by space.
    input: this is a test
    output: test a is this
    """
    s = Stack()
    for word in sentence.split(' '):
        s.push(word)

    tmp_list = []
    while s.size() > 0:
        tmp_list.append(s.pop())
    return ' '.join(tmp_list)


def test_reverse_by_words():
    sentence = 'this is a test'
    print('src text:', sentence)
    print('text reverse by words:', reverse_by_words(sentence))


def format_by_word_v1(content: str) -> str:
    """
    1. 只包含字母和数字
    2. 前一个为非字母和数字时，该字符转换为大写，其他字符转换为小写
    3. 转换后字符串如果首字母为大写，则转换为小写
    """
    ret = []
    is_change = False
    input = content.lower()
    for ch in input:
        if ch.isalnum():
            tmp = ch
            if ch.isalpha() and is_change:
                tmp = ch.upper()
            ret.append(tmp)
            is_change = False
        else:
            is_change = True
    if len(ret) == 0:
        return 'shop'

    if 65 <= ord(ret[0]) <= 90:  # 大写字母
        ret[0] = ret[0].lower()
    return ''.join(ret)


def format_by_word_v2(content: str) -> str:
    word = []
    words = []
    for ch in content:
        if ch.isalnum():
            word.append(ch)
        else:
            if len(word) > 0:
                words.append(''.join(word))
                word = []
    if len(word) > 0:
        words.append(''.join(word))

    if len(words) == 0:
        return 'shop'

    ret = []
    first_word = words[0]
    if first_word[0].isalpha():
        ret.append(first_word.lower())
    else:
        pos = 0
        for i in range(len(first_word)):
            if first_word[i].isdigit():
                pos += 1
        ret.append(first_word[:(pos + 2)] + first_word[(pos + 2):].lower())

    for word in words[1:]:
        if word[0].isalpha():
            word = word.title()
        else:
            word = word.lower()
        ret.append(word)
    return ''.join(ret)


def test_format_by_word():
    cases = []
    cases.append(('', 'shop'))
    cases.append(('_', 'shop'))
    cases.append(('hello_world', 'helloWorld'))
    cases.append(('Hello_World', 'helloWorld'))
    cases.append(('**Hello_worLD', 'helloWorld'))
    cases.append(('Hello_world_**python', 'helloWorldPython'))
    cases.append(('1Hello_worLD', '1HelloWorld'))
    cases.append(('1hello_1worLD', '1hello1world'))

    for input, expect in cases:
        res = format_by_word_v1(input)
        print('want:%s, got:%s' % (expect, res))
    print()

    for input, expect in cases:
        res = format_by_word_v1(input)
        assert res, expect
        print('want:%s, got:%s' % (expect, res))


if __name__ == '__main__':

    test_length_of_longest_unique_substring()
    print('py alg string demo done.')
