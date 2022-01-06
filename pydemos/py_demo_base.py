# -*- coding: utf-8 -*-
'''
Created on 2018-10-31
@author: zhengjin
'''

import copy
import getopt
import glob
import inspect
import importlib
import logging
import json
import re
import os
import random
import sys
import time
import datetime
import traceback

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from datetime import datetime as dt
from enum import Enum

print('python base demo INIT.')

logger = logging.getLogger(__name__)


def run_mod_imports():
    """
    use relative import ".module"

    NOTE: raise error ModuleNotFoundError when invoked from current py file.
    it's ok when invoked from [project-root]/main.py
    """
    from .imports import main
    main.run()


# examle 01, base
def py_base_ex01():
    # test for None
    flagObject = None
    if flagObject:
        print('object is not none.')
    else:
        print('object is none.')

    # search str by index or find
    def search_by_index(input_str):
        try:
            print(input_str[:input_str.index('g')])
        except ValueError as e:
            print(e)
    search_by_index('16g')
    search_by_index('32')

    def search_by_find(input_str):
        if input_str.find('g') == -1:
            print('search not found')
        else:
            print(input_str[:input_str.find('g')])
    print('')
    search_by_find('16g')
    search_by_find('32')


# example 02, print multiple lines
def py_base_ex02():
    lines = '\n'.join([
        'step1, this is the line one for test;',
        'step2, this is the line two for test;',
        'step3, this is the line three for test.',
    ])
    print(lines)
    print()

    lines = ('stepA, this is the line one for test;'
             'stepB, this is the line two for test;'
             'stepC, this is the line three for test.'
             )
    print(lines)

    # print random float number within range
    f = float('%.1f' % random.choice(np.arange(-2.0, 2.0, step=0.1)))
    print('float number with 1 decimal:', f)
    f = float('%.3f' % random.choice(np.arange(92., 94., step=0.001)))
    print('float number with 3 decimal:', f)


# example 03, import external modules
def py_base_ex03():
    sys.path.append(os.getenv('PYPATH'))
    from utils import Constants
    from utils import LogManager
    from utils import SysUtils

    try:
        logger = LogManager.build_logger(Constants.LOG_FILE_PATH)
        logger.info('import external modules test.')
        utils = SysUtils().get_instance()
        utils.run_sys_cmd('python --version')
    finally:
        LogManager.clear_log_handles()


# example 04, context current path
def py_base_ex04():
    # NOTE: context cur_path is the path where run cmd "python [script.py]"
    cur_path = os.getcwd()
    print('current path:', cur_path)

    f_path = os.path.abspath('../README.md')
    print('file exist check (%s):' % f_path, os.path.exists(f_path))


# example 05, parse command line args
def py_base_ex05():
    # "hi:o:": h => -h, i: => -i input_file, o: => -o output_file
    opts, _ = getopt.getopt(sys.argv[1:], 'hi:o:')

    if len(opts) == 0:
        usage()
        exit(0)

    input_file = ''
    output_file = ''
    for op, value in opts:
        if op == '-i':
            input_file = value
        elif op == '-o':
            output_file = value
        elif op == '-h':
            usage()
            exit(0)
    print('input file: %s, output file: %s' % (input_file, output_file))


def usage():
    lines = []
    lines.append('usage:')
    lines.append('-i: input file')
    lines.append('-o: output file')
    lines.append('-h: help')
    print('\n'.join(lines))


# example 06, plt chart line
def py_base_ex06():
    """
    pre-conditions: 
    $ pip install numpy
    $ pip install matplotlib
    """
    print('numpy version:', np.__version__)
    print('matplotlib version:', matplotlib.__version__)

    x_arr = [x for x in range(0, 10)]
    y_arr = [y for y in range(0, 20) if y % 2 == 0]
    z_arr = [y for y in range(0, 20) if y % 2 != 0]

    plt.title('Chart Test')
    ave_desc = 'y average: %d, z average: %d' % (
        np.average(y_arr), np.average(z_arr))
    plt.xlabel('X_label_text\n green: system_cpu, blue: user_cpu\n' + ave_desc)
    plt.ylabel('Y_label_text')

    plt.plot(x_arr, y_arr, color='red')
    plt.plot(x_arr, z_arr, color='blue')
    plt.grid(True, color='green', linestyle='--', linewidth='1')

    # plt.show()

    # default pixel [6.0,4.0]
    # if set dpi=100, image size 600*400
    # if set dpi=200, image size 1200*800
    # if set dpi=300，image size 1800*1200

    plt.tight_layout()
    plt.savefig(r'd:\profile.png', format='png', dpi=300)
    plt.close()


# example 07, plt chart spot
def py_base_ex07():
    # data
    # y_arr = [float(y) for y in range(0, 100) if y % 2 == 0]
    # x_arr = [x for x in range(0, len(y_arr))]

    n = 1024
    # 均值为0, 方差为1的随机数
    x_arr = np.random.normal(0, 1, n)
    y_arr = np.random.normal(0, 1, n)

    # 计算颜色值
    color = np.arctan2(x_arr, y_arr)
    # 绘制散点图
    plt.scatter(x_arr, y_arr, s=30, c=color, alpha=0.5)

    # 设置坐标轴范围
    plt.xlim((0, max(x_arr)))
    plt.ylim((0, max(y_arr)))

    # 不显示坐标轴的值
    plt.xticks(())
    plt.yticks(())

    plt.show()


# example 08_01, re.match() and re.search()
def py_base_ex08_01():
    print(re.match('super', 'superstition').span())  # (0, 5)
    print(re.match('super', 'insuperable'))  # None

    print(re.search('super', 'superstition').span())  # (0, 5)
    print(re.search('super', 'insuperable').span())  # (2, 7)


# example 08_02, reg exp
def py_base_ex08_02():
    """
    Get Java exceptions sum info from input content.
    """
    input_lines = []
    input_lines.append(
        'W System.err: org.json.JSONException: No value for preSaleSkuInfo')
    input_lines.append(
        'W System.err: Attempt to invoke virtual method \'int java.lang.String.length()\' on a null object reference')
    input_lines.append(
        'W System.err: net.grandcentrix.tray.core.TrayException: could not access stored data with uri')
    input_lines.append(
        'W System.err: org.json.JSONException: No value for preSaleSkuInfo')

    ret_dict = {}
    for line in input_lines:
        re_results = re.match(r'.*:\s+(.*Exception.{20,30})', line)
        exception_key = ''
        try:
            exception_key = re_results.group(1)
        except AttributeError as e:
            print(e)
            continue

        tmp_val = 0
        try:
            tmp_val = ret_dict[exception_key]
            ret_dict[exception_key] = tmp_val + 1
        except KeyError as e:
            print(e)
            ret_dict[exception_key] = 1

    print(ret_dict)


# example 09, list files by glob
def py_base_ex09():
    """
    get file path by glob (regexp pattern).
    """
    # "glob.glob" return list
    tmp_dir = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')
    files = glob.glob(tmp_dir + '/*.txt')
    print('\ntext files in tmp dir:', files)

    files = glob.glob(os.getcwd() + '/*.py')
    print('\npy files in current dir:', files)
    print()

    # "glob.iglob" return generator
    print('\ntext files in tmp dir:')
    for file in glob.iglob(tmp_dir + '/*.txt'):
        print(file)

    print('\npy files in current dir:')
    for file in glob.iglob(os.getcwd() + '/*.py'):
        print(file)


# example 10, list files in dir
def py_base_ex10():
    output_dir = os.path.join(os.getenv('PYPATH'), 'apitest/outputs')

    # 1: list subdirs and files, depth=1, return name
    print('\nresult files in outputs: ')
    for file in os.listdir(output_dir):
        print(file)

    # 2: list files by glob, depth=2, return abs path
    files = glob.glob(output_dir + '/*')
    files.extend(glob.glob(output_dir + '/*/*'))
    print('\nresult files in outputs by glob regexp: ')
    for file in files:
        if os.path.isfile(file):
            print('/' + file[file.find('outputs'):])
    print('total files:', len(files))

    # 3: list files by walk, depth=max
    print('\nresult files in outputs by walk:')
    total = 0
    # for dir_path, subpaths, files in os.walk(output_dir):
    for dir_path, _, files in os.walk(output_dir):
        for file in files:
            print(os.path.join(dir_path, file))
        total = total + len(files)
    print('total files:', total)


# example 11, collections deque
def py_base_ex11():
    from collections import deque
    names = ['jack', 'leo', 'sam', 'peter', 'jeo']
    deque_names = deque(names)
    deque_names.popleft()
    deque_names.appendleft('mark')
    print(deque_names)


# example 12, get sum of each color
def py_base_ex12():
    colors = ['red', 'green', 'red', 'blue', 'green', 'red']

    tmp_dict01 = {}
    for color in colors:
        tmp_dict01.setdefault(color, 0)
        tmp_dict01[color] += 1
    print(tmp_dict01)

    tmp_dict02 = {}
    for color in colors:
        tmp_dict02[color] = tmp_dict02.get(color, 0) + 1
    print(tmp_dict02)

    from collections import Counter
    count = Counter(colors)
    print(count)


# example 13, default dict
def py_base_ex13():
    from collections import defaultdict
    names = ['jack', 'leo', 'sam', 'peter', 'jeo']
    # set dict value default as list
    tmp_dict = defaultdict(list)
    for name in names:
        key = len(name)
        tmp_dict[key].append(name)
    print(tmp_dict)


# example 14, create dict from lists
def py_base_ex14():
    tmp_lst_ks = ['k1', 'k2', 'k3']
    tmp_lst_vs = ['v1', 'v2', 'v3']

    for k, v in zip(tmp_lst_ks, tmp_lst_vs):
        print('%s=%s' % (k, v))

    tmp_dict = dict([(k.upper(), v.upper())
                     for k, v in zip(tmp_lst_ks, tmp_lst_vs)])
    print('%s: %s' % (type(tmp_dict), tmp_dict))
    print()

    tmp_dict = {k.upper(): v.upper() for k, v in zip(tmp_lst_ks, tmp_lst_vs)}
    print('%s: %s' % (type(tmp_dict), tmp_dict))


# example 15, range by diff step
def py_base_ex15():
    alist = []
    for i in range(10):
        alist.append(i)
    print(alist)

    alist.clear()
    for i in range(10)[::-1]:
        alist.append(i)
    print(alist)

    alist.clear()
    for i in range(10)[::2]:
        alist.append(i)
    print(alist)


# example 16, pass var by value / reference
def py_base_ex16():
    def update_num(number):  # pass value
        number += 5

    def update_num_dict(number_dict):  # pass reference
        number_dict['value'] += 5

    def update_list(alist):  # pass reference
        alist.append(1)
        alist = [1, 2]

    number = 10
    update_num(number)
    print('number:', number)

    number_dict = {'value': 10}
    update_num_dict(number_dict)
    print('number value:', number_dict['value'])

    alist = []
    update_list(alist)
    print('list:', alist)


# example 17, decorator for class function
def py_base_ex17():
    def verify_dir_path(func):
        def _deco(*args, **kwargs):
            print('verify_dir_path args:', args)
            this = args[0]
            if not os.path.exists(this._dir_path):
                raise FileNotFoundError('dir path is not exist!')
            if not os.path.isdir(this._dir_path):
                raise IOError('dir path is not invalid!')
            return func(*args, **kwargs)

        return _deco

    class ListFile(object):
        def __init__(self, dir_path):
            self._dir_path = dir_path

        @verify_dir_path
        def listTextFiles(self):
            files = glob.glob(self._dir_path + '/*.txt')
            print('text files:', files)

        @verify_dir_path
        def listYmlFiles(self):
            files = glob.glob(self._dir_path + '/*.yml')
            print('yml files:', files)

    list_file = ListFile(os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files'))
    list_file.listTextFiles()
    list_file.listYmlFiles()


# example 18, keyword *args
def py_base_ex18():
    test_lst = ['a', 'b', 'c']

    # as input param
    def print_abc(a, b, c):
        print(f'a={a}, b={b}, c={c}')
    print_abc(*test_lst)

    # as declare param
    def print_vals(*args):
        print('type:', type(args))
        print(f'input arguments: {args}')
    print_vals(1, 2, 3)
    print_vals(test_lst)
    print_vals(*test_lst)


# example 19, json parse
def py_base_ex19():
    input_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files/test.json')
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)

    json_text = ''
    with open(input_path, 'r') as f:
        json_text = f.read()

    if len(json_text) > 0:
        json_object = json.loads(json_text)
        print('request id:', json_object['requestId'])
        print('instance job:',
              json_object['rawInstances'][0]['rawFeatures']['job'])


# example 20, append content to file
def py_base_ex20():
    file_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files/test.file')

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, 'a', encoding='utf-8') as f:
        lines = ['\npython test write chinese words.\n']
        lines.append('写入中文到文件测试1\n')
        f.writelines(lines)
        f.write('写入中文到文件测试2\n')


# example 21, multi process
def py_base_ex21():
    from multiprocessing import Process

    class MyProcess(Process):
        def __init__(self, tag):
            super().__init__()  # super.init() should be invoked
            self._tag = tag

        def run(self):
            print('%s => pid=%d, name=%s is running ...' %
                  (self._tag, os.getpid(), self.name))
            time.sleep(3)

    p = MyProcess('test')
    print('process start')
    p.start()

    print('main=%d, wait for process done' % os.getpid())
    p.join(timeout=3)
    time.sleep(1)
    if p.is_alive():
        p.kill()


# example 22, py tips
def py_base_ex22():
    # 序列解包
    def tip_test01():
        user_ls = ['henry', 18, 'male']
        name, age, gender = user_ls
        print('name=%s, age=%d, male=%s' % (name, age, gender))
    tip_test01()

    # 判断是否为空列表, 空字典, 空字符串
    def tip_test02():
        l, d, s = [1, 2, 3], {}, ''
        if l:
            print('list is not empty')
        if d:
            print('dict is not empty')
        if s:
            print('string is not empty')
    tip_test02()

    # 判断诸多条件是否至少有一个成立
    def tip_test03():
        math, physics, computer = 70, 40, 80
        if any([math < 60, physics < 60, computer < 60]):
            print('not pass')
    tip_test03()

    # 判断诸多条件是否全部成立
    def tip_test04():
        math, physics, computer = 70, 70, 80
        if all([math >= 60, physics >= 60, computer >= 60]):
            print('pass')
    tip_test04()

    # 过滤数字并求和
    def tip_test05():
        lst = [1, 2, 3, 'a', 'b', 4, 5.0]
        count = sum([i for i in lst if type(i) in (int, float)])
        print('count = %.1f' % count)
    tip_test05()


# example 23, process bar
def py_base_ex23_01():
    i, n = 0, 100
    for i in range(n):
        time.sleep(0.1)
        if (i + 1) % 10 == 0:
            print(str(i + 1) + '%', end='\r')


def py_base_ex23_02():
    def process_bar(num, total):
        rate = float(num) / total
        rate_num = int(100 * rate)
        r = '\r[%s%s]%d' % (
            ('*' * rate_num), (' ' * (100 - rate_num)), rate_num)
        sys.stdout.write(r + '%')
        sys.stdout.flush()

    i, n = 0, 100
    for i in range(n):
        time.sleep(0.1)
        process_bar(i + 1, n)


# example 24, value and reference
def py_base_ex24():
    # 1: list
    def update_list(lst):
        lst[2] = 30
        print("[update]", lst)

    lst = [1, 2, 3, 4, 5]
    print("\nsrc list:", lst)

    lst2 = lst
    lst[0] = 10
    lst2[1] = 20
    update_list(lst)
    print("lst: %r, lst2: %r" % (lst, lst2))

    # 2: map
    def update_map(m):
        m[3] = "THREE"
        print("[update]", m)

    m = {1: "one", 2: "two", 3: "three"}
    print("\nsrc map:", m)

    m2 = m
    m[1] = "ONE"
    m2[2] = "TWO"
    update_map(m)
    print("map: %r, map2: %r" % (m, m2))

    # 3: object
    class person(object):
        def __init__(self, name, age, job):
            self.name = name
            self.age = age
            self.job = job

        def __str__(self):
            return "name=%s, age=%d, job=%s" % (self.name, self.age, self.job)

    def update_person(person):
        person.job = "TESTER"
        print("[update]", person)

    p = person("Henry", 30, "tester")
    print("\nsrc person:", p)

    p1 = p
    p.name = "HENRY"
    p1.age += 1
    update_person(p)
    print("p: %s, p1:%s" % (p, p1))


# example 25, datetime
def py_base_ex25():
    def print_next_day(timestamp):
        next_day_timestamp = timestamp + datetime.timedelta(days=1)
        next_date = dt.strftime(next_day_timestamp, '%Y-%m-%d')
        print(next_date)

    print('\ntomorrow date:')
    now_timestamp = dt.now()
    print_next_day(now_timestamp)
    print('next day for 20190831:')
    test_timestamp = dt.strptime('20190831', '%Y%m%d')
    print_next_day(test_timestamp)

    def print_days(s_date, e_date):
        s_date_timestamp = dt.strptime(s_date, '%Y-%m-%d')
        e_date_timestamp = dt.strptime(e_date, '%Y-%m-%d')
        while s_date_timestamp <= e_date_timestamp:
            print("day:", dt.strftime(s_date_timestamp, '%Y%m%d'))
            s_date_timestamp += datetime.timedelta(days=1)

    print('\ndays between 2019-08-27 and 2019-09-02:')
    print_days('2019-08-27', '2019-09-02')


# example 26, 2d array by numpy
def py_base_ex26():
    array_2d = np.zeros((2, 5))
    for i in range(5):
        array_2d[0][i] = i
    print(array_2d)


# example 27, field type hint
def py_base_ex27_01():
    def addTwo(x: int) -> int:
        return x+2
    print('results:', addTwo(10))


def py_base_ex27_02():
    import pprint
    from typing import List

    Vector = List[float]
    Matrix = List[Vector]

    def addMatrix(a: Matrix, b: Matrix) -> Matrix:  # type hint
        result = []
        for i, row in enumerate(a):
            result_row = []
            for j, row in enumerate(row):
                result_row += [a[i][j] + b[i][j]]  # instead of list.append()
            result += [result_row]
        return result

    x = [[1.0, 2.0], [3.0, 4.0]]
    y = [[2.0, 2.0], [-3.0, -3.0]]
    res = addMatrix(x, y)
    print('print:', res)
    pprint.pprint(res)  # print复杂对象


# example 28, deco 类装饰器
def py_base_ex28():
    import functools

    class MyLogging(object):
        def __init__(self, level='warn'):
            self.level = level

        def __call__(self, func):
            @functools.wraps(func)
            def _deco(*args, **kwargs):
                if self.level == 'warn':
                    self.notify(func)
                return func(*args, **kwargs)
            return _deco

        def notify(self, func):
            print('%s is running' % func.__name__)

    @MyLogging(level='warn')  # 执行__call__方法
    def bar(a, b):
        print('i am bar: %d' % (a+b))

    bar(1, 2)


# example 29, iterable and iterator
def py_base_ex29():
    from collections.abc import Iterable, Iterator

    mylist = ['a', 'b', 'c']
    print('isinstance(mylist, Iterable):', isinstance(mylist, Iterable))
    print('isinstance(mylist, Iterator):', isinstance(mylist, Iterator))

    myiter = iter(mylist)
    print('\nmyiter:', myiter)
    print('isinstance(myiter, Iterable):', isinstance(myiter, Iterable))
    print('isinstance(myiter, Iterator):', isinstance(myiter, Iterator))

    mygen = (x for x in mylist)
    print('\nmygen:', mygen)
    print('isinstance(mygen, Iterable):', isinstance(mygen, Iterable))
    print('isinstance(mygen, Iterator):', isinstance(mygen, Iterator))

    # file is both iterable and iterator
    with open('data/data.log', mode='r', encoding='UTF-8') as f:
        print('\nfile:', f)
        print('isinstance(f, Iterable):', isinstance(f, Iterable))
        print('isinstance(f, Iterator):', isinstance(f, Iterator))

        print('\nfile content:')
        for line in f:
            print(line.rstrip('\n'))


# example 30, py tips
def py_base_ex30():
    # decimal
    from decimal import Decimal
    assert Decimal('0.1') + Decimal('0.2') == Decimal('0.3')

    # 列表的扁平化
    groups = [['x1', 'x2'], ['y1', 'y2'], ['z']]
    names = sum(groups, [])
    print('names:', names)


# example 31, *args and **kwargs
def py_base_ex31():
    # 1
    def _sum(*args):
        print(f'\nfunc args, type={type(args)}, value={args}')
        return sum(args)

    print('*args func args, and return:', _sum(1, 2, 3))

    # 2
    def _add(a, b, c=1):
        print(f'\ninput args: a={a}, b={b}')
        return a + b + c

    tmp_list = [1, 2]
    print('*args as func input, and return:', _add(*tmp_list))
    tmp_dict = {'b': 1, 'a': 6}
    print('**kwargs as func input, and return:', _add(**tmp_dict))

    # list to tuple
    def _print(*val):
        print('\ninput args type:', type(val))
        print('input values:', val)

    vals = ['a', 'b', 'c']
    _print(*vals)


# example 32, field type assert
def py_base_ex32():
    words = ('11.11', '3.0', '10', '-1', '0', 'a')
    uints = [word for word in words if word.isdigit()]
    print('uints:', uints)

    words = (11.11, 3.0, 10, -1, 0, 'a')
    ints = [w for w in words if type(w) in (int,)]
    print('ints:', ints)

    nums = [w for w in words if isinstance(w, (int, float))]
    print('numbers:', nums)


# example 33, memory size
def dump_object(obj):
    for attr in dir(obj):
        print('obj.%s=%s' % (attr, getattr(obj, attr)))


def get_size(obj, seen=None):
    # From https://goshippo.com/blog/measure-real-size-any-python-object/
    # Recursively finds size of objects
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0

    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


class DataItem1(object):
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address


class DataItem2(object):
    __slots__ = ['name', 'age', 'address']  # 指定类属性列表

    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address


def py_base_ex33():
    d1 = DataItem1('Alex', 42, '-')
    d2 = DataItem1('Boris', 24, 'In the middle of nowhere')

    dump_object(d1)
    print()

    print('sys.getsizeof(d1):', sys.getsizeof(d1))
    print('sys.getsizeof(d2):', sys.getsizeof(d2))
    print()

    print('get_size(d1):', get_size(d1))
    print('get_size(d2):', get_size(d2))
    d1.weight = 66
    print('get_size(d1):', get_size(d1))
    print()

    d3 = DataItem2('Alex', 42, '-')
    d4 = DataItem2('Boris', 24, 'In the middle of nowhere')
    print('get_size(d1):', get_size(d3))
    print('get_size(d2):', get_size(d4))


# example 34, remove /r in file content
def py_base_ex34():
    in_file = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/data.txt')
    out_file = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/test.out')
    replace_r_v2(in_file, out_file)


def replace_r(in_file, out_file):
    if not os.path.exists(in_file):
        raise FileNotFoundError('file not found: ' + in_file)

    print('remove (\\r) in file content')
    with open(in_file, 'rb') as in_file, open(out_file, 'wb') as out_file:
        content = in_file.read()
        replaced = content.replace(b'\r', b'')
        out_file.write(replaced)


def replace_r_v2(in_file, out_file):
    """
    1. 读取时, 不指定newline, 则默认开启"Universal new line mode", 所有'\n', '\r', or '\r\n'被默认转换为'\n'
    2. 写入时, 不指定newline, 则换行符为各系统默认的换行符（'\n', '\r', or '\r\n' ）;
    指定为newline='\n', 则都替换为'\n'（相当于Universal new line mode）
    3. 不论读或者写时, newline=''都表示不转换
    """
    if not os.path.exists(in_file):
        raise FileNotFoundError('file not found: ' + in_file)

    print('remove (\\r) in file content')
    with open(in_file, 'r') as in_file, open(out_file, 'w', newline='\n') as out_file:
        content = in_file.read()
        out_file.write(content)


# example 35, read big file
def py_base_ex35():
    def gen_file(file_path):
        with open(file_path, 'r+') as f:
            line = f.readline()
            while line:
                yield line.strip()
                line = f.readline()

    input_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files', 'data.csv')
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)

    print(f'read big file ({input_path}):')
    for line in gen_file(input_path):
        print(line)


# example 36, list
def py_base_ex36():
    test_list = ['a', 'b', 'd']

    # insert item
    test_list.insert(2, 'c')
    print(test_list)

    # remove item
    test_list.remove('b')
    print(','.join(test_list))

    # iterator with index
    for idx, val in enumerate(test_list):
        print('iterator at %d: %s' % (idx, val))


# example 38, read chrome cookie (sqlite.db)
def py_base_ex38():
    """
    path: /Users/jinzheng/Library/Application Support/Google/Chrome/Profile 1/Cookies

    sqlite cmd:
    .header on 启用表头
    .mode column 使用列模式
    .quit

    sql:
    select host_key,name,encrypted_value from cookies where name in ("SID","HSID");
    """
    import sqlite3

    c_path = '/tmp/Cookies.db'
    if not os.path.exists(c_path):
        print('file not exist:', c_path)
        return

    conn = sqlite3.connect(c_path)
    cursor = conn.cursor()

    sql = "select host_key,name,value,expires_utc,encrypted_value from cookies where name = 'SID';"
    results = cursor.execute(sql).fetchall()
    print(results)

    cursor.close()
    conn.close()


# example 39, read chrome cookie (sqlite.db)
def py_base_ex39():
    """
    refer to:
    https://github.com/n8henrie/pycookiecheat

    dependency lib:
    pip install pycookiecheat

    cmd:
    cp ${HOME}/Library/Application\\ Support/Google/Chrome/Profile\\ 1/Cookies /tmp/Cookies.db
    chmod 644 /tmp/Cookies.db
    """
    import requests
    from pycookiecheat import chrome_cookies

    c_path = '/tmp/Cookies.db'
    if not os.path.exists(c_path):
        print('file not exist:', c_path)
        return

    url = 'https://docs.google.com/presentation/d/1GAByZxeqd7VzG_QoPjvNTgsnSc7xb3Tj_m7sIb6x1ZY/edit#slide=id.g87a7ccd906_0_56'
    cookies = chrome_cookies(url=url, cookie_file=c_path)
    print(f"cookie from {url}:")
    print(cookies)


# example 40, 拼接 dict
def py_base_ex40():
    t_dict = {
        "header": {
            "code": 0
        },
        "data": {
            "key1": "value1"
        }
    }

    data_dict = dict(**t_dict["data"], key2="value2")
    result_dict = dict(header=t_dict["header"], data=data_dict)
    print(result_dict)


# example 41, attr and inspect
def py_base_ex41():

    class MyObject(object):
        static_field = 'static_field'

        def __init__(self):
            self.field = 'instance_field'

        def echo(self):
            print(self.static_field, self.field)

    print('\nobject inspect:')
    obj = MyObject()
    own_attrs = [attr for attr in dir(obj) if not attr.startswith('__')]
    for attr in own_attrs:
        val = getattr(obj, attr)
        if inspect.ismethod(val):
            print(f"method:{attr}")
        else:
            print(f"field:{attr}={val}")

    m = {'key1': 'value1', 'key2': 'value2'}
    methods = [attr for attr in dir(m) if not attr.startswith(
        '__') and inspect.isbuiltin(getattr(m, attr))]
    print('\nmap built in methods:', methods)


# example 42, py typing
def py_base_ex42():
    from typing import Callable, List, Union

    def foo():
        print('foo')

    def bar():
        print('bar')

    my_list: List[Union[str, Callable]] = []
    my_list.append(foo)
    my_list.append('test')
    my_list.append(bar)

    for item in my_list:
        if callable(item):
            print('function:', item.__name__)
        else:
            print('string:', item)


# example 43, deco with parameters
def py_base_ex43():
    def wrap(author='vieira'):
        def _deco(func):
            # add a attribute

            def _inner_deco():
                # add hooks
                print('\npre-hook')
                ret = func()
                print('after-hook')
                return ret

            setattr(_inner_deco, 'author', author)
            return _inner_deco

        return _deco

    @wrap(author='zj')
    def say_hello():
        print('say_hello invoked')
        return 'hello'

    assert hasattr(say_hello, 'author')
    print(say_hello(), say_hello.author)


# example 44, reflect for func by inspect
def py_base_ex44():
    def div(a, b=1):
        return a / b

    func_sig = inspect.signature(div)
    func_parameters = list(func_sig.parameters.values())
    print('\nfunc:', div.__name__)
    for p in func_parameters:
        default = p.default
        if default == inspect._empty:
            default = 'empty'
        kind = str(p.kind)
        print(f"param={p.name}, default={default}, type={kind}")


# example 45, load module from py file by importlib
def py_base_ex45():
    def printTestClass(imported):
        clazz = [item.__name__ for item in vars(imported).values() if inspect.isclass(
            item) and item.__name__.lower().startswith('test')]
        print('test classes:', clazz)

    def printTestMethod(clazz):
        methods = [item.__name__ for item in vars(clazz).values() if callable(
            item) and item.__name__.lower().startswith('test')]
        print('test methods:', methods)

    # 1
    file_name = 'py_ut_selenium.py'
    file_path = os.path.abspath(file_name)
    file_dir = os.path.dirname(file_path)
    mod_name = os.path.splitext(file_name)[0]
    print(f'\nfilepath={file_path}, filedir={file_dir}, modname={mod_name}')

    source = importlib.machinery.SourceFileLoader(mod_name, file_path)
    print(type(source))
    imported = source.load_module(mod_name)
    print(type(imported))
    printTestClass(imported)
    print()

    # 2
    mod = importlib.import_module(mod_name)
    print(type(mod))
    printTestClass(mod)
    printTestMethod(mod.TestPy01)
    print()

    # 3, 'imp' is deprecated
    import imp
    mod = imp.load_source('test_import_mod', file_path)
    print(type(mod))
    printTestClass(mod)
    printTestMethod(mod.TestPy01)


# example 46, py tips
def py_base_ex46():
    def printDict(in_dict):
        print('dict:', ','.join([f'{k}={v}' for k, v in in_dict.items()]))

    # dict init
    d1 = {'k1': 'v1', 'k2': 'v2'}
    printDict(d1)
    d2 = dict(k3='v3', k4='v42')
    printDict(d2)
    print()

    # get 1st value
    lst = []
    lst.append(('v1', 'v2', 'v3'))
    lst.append(('k1', 'k2', 'k3'))
    for val, *_ in lst:
        print(val)
    print()

    # load json file
    with open('/tmp/test/test.json', mode='r') as f:
        input = json.load(f)
        printDict(input)


# example 47, get python run stack context
def py_base_ex47():
    stacks = inspect.stack()
    for stack in stacks:
        script_path = stack.filename
        script_name = script_path[script_path.rfind('/') + 1:]
        function_name = stack.function
        context_dict = {
            'file': script_name,
            'function': function_name
        }
        print(json.dumps(context_dict))


# example 48, assert
def py_base_ex48():
    s = 'a' and 'b'
    print('\nresult:', s)

    s = 'a' or 'b'
    print('result:', s)

    s = '' or 'default'
    print('result:', s)


# example 49, status by binary
class Operation(object):
    Create = 1
    Write = 1 << 1
    Remove = 1 << 2
    Rename = 1 << 3

    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: int):
        self._value += val

    def has_create(self):
        return True if self._value & self.Create != 0 else False

    def has_wirte(self):
        return True if self._value & self.Write != 0 else False

    def __str__(self):
        ret = ''
        if (self._value & self.Create) == self.Create:
            ret += '|Create'
        if (self._value & self.Write) == self.Write:
            ret += '|Write'
        if (self._value & self.Remove) == self.Remove:
            ret += '|Remove'
        if (self._value & self.Rename) == self.Rename:
            ret += '|Rename'
        return ret[1:]


def py_base_ex49():
    print('\nall operations: create=%s, write=%s, remove=%s, rename=%s'
          % (bin(Operation.Create), bin(Operation.Write), bin(Operation.Remove), bin(Operation.Rename)))
    op = Operation()
    op.value = Operation.Create
    op.value = Operation.Remove
    op.value = Operation.Rename
    print('has create:', op.has_create())
    print('has write:', op.has_wirte())
    print('cur op:', op)


# example 50, enum
class Color(Enum):
    red = 1
    orange = 2
    yellow = 3
    green = 4
    blue = 5
    indigo = 6
    purple = 7


def py_base_ex50():
    print('\navailable colors:')
    for color in Color:
        print(color.name, color.value)


# expample 51, map operations
def py_base_ex51():
    from typing import Text, Any, Dict

    src: Dict[Text, Any] = {}
    src['1st'] = 1
    src['2nd'] = 2
    src['3rd'] = 3

    # copy and update
    new_dict = {
        '1st': 'one',
        '4th': 'four',
    }
    dst = copy.copy(src)
    dst.update(new_dict)

    print('\nsrc:', src)
    print('dst:', dst)

    # pop
    key = '2nd'
    print(f'dst pop {key}:{dst.pop("2nd")}')
    print('dst:', dst)

    # get first kv
    k, v = list(dst.items())[0]
    print(f'first item: {k}:{v}')


# expample 52, object dyn attrs
def py_base_ex52():
    class MyStudent(object):
        def __init__(self, uid, name):
            self._uid = uid
            self._name = name

        def __repr__(self):
            ret = []
            for k in vars(self):
                ret.append('%s:%s' % (k, getattr(self, k)))
            return '|'.join(ret)

    s = MyStudent(1, 'foo')
    print('\nstudent info:', s)

    s = MyStudent(2, 'bar')
    s.age = 23
    setattr(s, 'major', 'computer')
    print('student info:', s)


# expample 53, with context
def py_base_ex53():
    import contextlib

    @contextlib.contextmanager
    def run_time_context():
        print('\nbefore mock start')
        start = time.time()
        yield
        print('after mock end')
        print('exec duration: %ds' % int(time.time() - start))

    # 并发安全
    with run_time_context():
        print('mock start')
        time.sleep(3)
        print('mock end')


# expample 54, get week of year
def py_base_ex54():
    now = dt.now()
    print('\ncurrent date:', dt.strftime(now, '%Y-%m-%d'))
    print('current date without leading zero:', dt.strftime(now, '%Y-%-m-%-d'))

    print('\nweek of year:', dt.strftime(now, '%Y-%V'))
    res = datetime.date(now.year, now.month, now.day).isocalendar()
    print('week of year:', res[1])


# expample 55, calculate delta date
def py_base_ex55():
    target_ts = dt.strptime('20210823', '%Y%m%d')
    cur_ts = dt.now()
    delta = target_ts - cur_ts
    print('\ndelta days:', delta.days)

    test_ts = dt.strptime('20210816', '%Y%m%d')
    delta = test_ts - target_ts
    print('delta days:', delta.days)


# expample 56, init object by dict
def py_base_ex56():
    class TestEntry(object):
        def __init__(self):
            self.ticket_key = 'na'
            self.ticket_name = 'na'

        def __str__(self):
            return f'tkey={self.ticket_key}, tname={self.ticket_name}'

    d = {
        'ticket_key': 'key-001'
    }
    entry = TestEntry()
    entry.__dict__.update(d)
    print('\nentry:', entry)


# expample 57, json dump object
def py_base_ex57():
    class Student(object):
        def __init__(self, name, age):
            self.name: str = name
            self.age: int = age

        def __str__(self):
            return f'name={self.name},age={self.age}'

    # object -> dict -> str
    s = Student('foo', 11)
    s_str = json.dumps(s.__dict__, indent=2)
    print('\nstudent string:', s_str)

    # str -> dict -> object
    s_str = s_str.replace('foo', 'bar')
    s_dict = json.loads(s_str)
    s.__dict__.update(s_dict)
    print('student object:', s)


# expample 58, deep copy
def py_base_ex58():
    skills = ['java', 'golang', 'js']
    p = {
        'name': 'foo',
        'age': 30,
        'skills': skills,
    }

    print('\nbefore update')
    p1 = copy.copy(p)
    p2 = copy.deepcopy(p)
    print(json.dumps(p1))
    print(json.dumps(p2))

    skills.append('rust')
    print('\nafter update')
    print(json.dumps(p1))
    print(json.dumps(p2))


# expample 59, load module and run func
def py_base_ex59():
    test_script = """# coding=utf-8
import os
# error: No module named 'x'
# import x.y.z

def hello_foo():
    print('foo')

def hello_bar():
    print('pwd:', os.getcwd())
    return 'bar'
"""
    file_path = '/tmp/test/hello.py'
    with open(file_path, mode='w') as f:
        f.write(test_script)

    mod_name, suffix = os.path.splitext(os.path.basename(file_path))
    print(f'\nload: file={mod_name}{suffix},module_name={mod_name}')
    source = importlib.machinery.SourceFileLoader(mod_name, file_path)
    imported = source.load_module(mod_name)

    fns = [item for item in vars(imported).values() if callable(item)]
    print('func:', [fn.__name__ for fn in fns])
    for fn in fns:
        if 'foo' in fn.__name__:
            print('\ncall foo func:')
            fn()
        if 'bar' in fn.__name__:
            print('\ncall bar func:')
            print(fn())


# expample 60, default invoke
def py_base_ex60():
    def hello():
        print('call')
        return 'hello'

    # dict get() 返回默认值 => always invoke
    d = {
        '1': 'one',
        '3': 'three'
    }
    print('\ndict values:')
    for i in ('1', '2', '3'):
        print(d.get(i, hello()))
    print()

    # 默认参数 => invoke once when method declare
    def say_hello(text=hello()):
        print('hello,', text)

    say_hello('foo')
    say_hello('bar')


# expample 61, bean object, and remove when iterator
def py_base_ex61():
    class StudentBean(object):
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def __str__(self):
            return f'name={self.name},age={self.age}'

    students = []
    for idx, val in enumerate('abcdefg'):
        students.append(StudentBean(f'{val}_{val}', idx+30))
    keys_to_remove = ['a', 'b', 'd', 'e']

    for s in students:
        print(s)
    print()

    # NOTE: do not remove item when iterator
    for s in students:
        print('iterator:', s.name)
        if s.name[0] in keys_to_remove:
            print('remove:', s.name)
            students.remove(s)
    print()

    # ok to remove
    students_to_remove = [s for s in students if s.name[0] in keys_to_remove]
    for s in students_to_remove:
        students.remove(s)

    # print bean object as dict
    for s in students:
        print(s.__dict__)


# expample 62, python3 custom sort string list
def py_base_ex62():
    level_value_dict = {
        'na': 0,
        'low': 1,
        'mid': 2,
        'high': 3,
    }

    def mycmp(x, y):
        x_value = level_value_dict[x]
        y_value = level_value_dict[y]
        return y_value - x_value

    from functools import cmp_to_key
    key = cmp_to_key(mycmp)
    rows = ['low', 'high', 'low', 'high', 'mid', 'low', 'na', 'mid']
    res = sorted(rows, key=key)
    print('result:', ','.join(res))


# expample 63, lambda
def py_base_ex63():
    """
    lambda 函数只能写一个表达式，这个表达式的执行结果就是函数的返回值，不用写 return 关键字。
    """
    # 闭包问题
    def multiply_v1():
        return [lambda x: i * x for i in range(4)]
    res = [m(100) for m in multiply_v1()]
    print(res)

    # fix: use generator instead of list
    def multiply_v2():
        return (lambda x: i * x for i in range(4))
    res = [m(100) for m in multiply_v2()]
    print(res)


# expample 98, regexp samples
def py_base_ex98():
    # match: 返回匹配上的第一个字串。需要注意的是 match 函数是从字符串开始处开始查找的，如果开始处不匹配
    # search: 函数类似于 match, 不同之处在于不限制正则表达式的开始匹配位置
    # findall: 寻找所有匹配正则表达式的字串，返回一个列表
    # finditer: findall 返回一个列表， finditer 返回一个迭代器
    def get_node_id():
        test_str = '/jenkins/job/Test%20Workflow/16/execution/node/6/wfapi/describe'
        regexp = re.compile(r'node/(?P<node_id>\d+)/')
        m = regexp.search(test_str)
        if m:
            print('\nregexp results:')
            print(m.group())
            print(m.groups())
            print(m.groupdict('default'))
    get_node_id()

    def get_title_tags():
        test_str = '[AS][BE][TH]Merchant portal send noti to partner app users'
        regexp = re.compile(r'(\[\w+\])')
        res = regexp.findall(test_str)
        print('\nregexp results:')
        print(' | '.join(res))
    get_title_tags()

    def get_item_number():
        test_str = 'https://jenkins.i.test.com/queue/item/564210/'
        regexp = re.compile(r'item/(\d+)/$')
        m = regexp.search(test_str)
        if m:
            print('\nqueue item id:', m.groups()[0])
    get_item_number()

    def email_validate():
        regexp = re.compile('com.+$')
        print('\nvalidate emails:')
        for test_str in ('tester@mailserver.com_783c77ab-4e2f', 'tester@mailserver.com#1'):
            print(re.sub('com.+$', 'com', test_str))
            print(regexp.sub('com', test_str))
    email_validate()

    def check_no_mr(text):
        text = text.lower()
        regexp = re.compile('no.*mr')
        m = regexp.search(text)
        return True if m else False
    print('\nno mr check results:')
    for text in ('no-mr', 'NO-mr', 'NO_MR', 'noMr', 'test'):
        print(f'text:{text}, result:{check_no_mr(text)}')

    def check_app_tag(text):
        text = text.lower()
        regexp = re.compile('andorid|ios')
        m = regexp.search(text)
        return True if m else False
    print('\napp tag check results:')
    for text in ('[is][Andorid]', '[iOS][pay]', '[be][wallet]'):
        print(f'text:{text}, result:{check_app_tag(text)}')


# expample 99, common
def py_base_ex99():
    # title
    print('samuel colvin'.title())
    print()

    # 泰文 bytes 转 str
    s = b'\340\271\204\340\270\241\340\271\210\340\270\252\340\270\262\340\270\241\340\270\262\340\270\243\340\270\226\340\271\203\340\270\212\340\271\211\340\270\204\340\270\271\340\270\233\340\270\255\340\270\207\340\270\231\340\270\265\340\271\211'
    print(s.decode())
    print()

    # dict as input params
    def my_print(name='default', age=1):
        print(f'name={name}, age={age}')

    test_data = {'name': 'foo', 'age': 30}
    my_print(**test_data)
    print()

    # 推导式
    tmp = {x for x in 'hello world' if x not in 'abcdefg'}
    print(type(tmp), tmp)
    print()

    # 类型判断
    print(isinstance(1, int))
    print(isinstance(1.0, float))
    print(isinstance(0.9, (int, float)))
    print(isinstance('t', (int, float)))


if __name__ == '__main__':

    # run_mod_imports()

    def get_parent(path, level):
        for _ in range(level):
            path = os.path.dirname(path)
        return path

    print('python base demo START.')
    print('\npython version:\n', sys.version)

    pypath = os.getenv('PYPATH') if len(os.getenv('PYPATH')) > 0 else 'null'
    print('PYPATH=' + pypath)

    project_path = get_parent(os.path.abspath(__file__), 2)
    print('PROJECT_ROOT=' + project_path)

    # 使用 logger 方式打印字符串，可以避免不必要的字符串解析，提高性能
    logger.warning(
        'this is logger print: str=%s, number=%d, float=%.2f', 'helloworld', 123, 11.337)
    print()

    try:
        py_base_ex56()
    except:
        traceback.print_exc()

    print('python base demo DONE.')
