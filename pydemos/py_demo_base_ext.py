# coding=utf-8
# pylint: disable=W0212,W0612,W0702

import contextlib
import copy
import datetime
import functools
import importlib
import inspect
import json
import os
import re
import time
import traceback
from collections import Counter, OrderedDict, defaultdict, namedtuple
from dataclasses import dataclass, field
from datetime import datetime as dt
from enum import Enum
from typing import Any, Dict, List, Text


def py_demo_if_cond():
    s = 'a' and 'b'
    print('\nresult:', s)  # b

    s = 'a' or 'b'
    print('result:', s)  # b

    s = '' or 'default'  # b
    print('result:', s)


def py_demo_calculate():
    i = 12 // 5
    print('math int div result:', i)

    i = 5**2
    print('math power result:', i)

    bin_str = '0111'
    i = int(bin_str, 2)
    print(f'binary {bin_str} -> int {i}')


def py_demo_f_print():
    x = 10
    y = 20
    print(f'float x: {x:.2f}')
    print(f'hex x: {x:#0x}')
    print(f'bin x: {x:b}')
    print(f'x * y = {x * y}')
    print()

    now = dt.now()
    print(f'date time: {now:%m-%d-%Y %H:%M:%S}')
    print(f'week day: {now:%A}')
    print(f'day of year: {now:%j}')
    print()

    num = 4
    print(f'number is: {num:4}')
    for idx in range(1, 5):
        print(f'the number is: {num:{idx}}')
    print(f'number: {num:<4}eof')  # left align
    print(f'number: {num:>4}eof')  # right align
    print(f'number: {num:^4}eof')  # center align
    print()

    @dataclass
    class Person:
        name: str
        age: int = 1

        def __str__(self) -> str:
            return f'{self.name} is {self.age} years old'

    p = Person('foo', 31)
    print(f'str: {p}')
    print(f'repr: {p!r}')


def py_demo_default_call():
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

    # say_hello('foo')
    # say_hello('bar')


def py_demo_object_dyn_attrs():
    # pylint: disable=W0201
    class MyStudent(object):
        def __init__(self, uid, name):
            self._uid = uid
            self._name = name

        def __repr__(self):
            ret = []
            for k in vars(self):
                ret.append('%s:%s' % (k, getattr(self, k)))
            return '|'.join(ret)

    st = MyStudent(1, 'foo')
    print('\nstudent info:', st)

    st = MyStudent(2, 'bar')
    st.age = 23
    setattr(st, 'major', 'computer')
    print('student info:', st)


def py_demo_deep_copy():
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


def py_demo_with_context():
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


# list, dict

def py_demo_dict_op():
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


def py_demo_merge_dicts_01():
    # 1: create dict from list
    class num(object):
        def __init__(self, name, value):
            self.name = name
            self.value = value

    numbers = [
        num('one', 1),
        num('two', 2),
        num('three', 3),
        num('four', 4),
        num('five', 5),
    ]
    d = {num.name: num.value for num in numbers}
    print(type(d))
    for k, v in d.items():
        print(f'{k}:{v}')
    print()

    # 2: merge 2 dict
    # NOTE: dict key must be string
    dict_a = {'1': 'one'}
    dict_b = {
        '2': 'two',
        '3': 'three',
    }
    dict_all = dict(**dict_a, **dict_b)
    print(dict_all)


def py_demo_merge_dicts_02():
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


def py_demo_collection_tip():
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
    with open('/tmp/test/test.json', mode='r', encoding='utf8') as f:
        data = json.load(f)
        printDict(data)


# enum

def py_demo_enum_declare():
    class Color(Enum):
        red = 1
        orange = 2
        yellow = 3
        green = 4
        blue = 5
        indigo = 6
        purple = 7

    print('\navailable colors:')
    for color in Color:
        print(color.name, color.value)


# json

def py_demo_init_object_by_dict():
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


def py_demo_object_json_dump():
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


# iterator

def py_demo_iterator_and_remove():
    # pylint: disable=W4701
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


# lambda 函数只能写一个表达式，这个表达式的执行结果就是函数的返回值，不用写 return 关键字。

def py_demo_lambda():
    # pylint: disable=W0640
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


# date

def py_demo_get_week_of_year():
    now = dt.now()
    print('\ncurrent date:', dt.strftime(now, '%Y-%m-%d'))
    print('current date without leading zero:', dt.strftime(now, '%Y-%-m-%-d'))

    print('\nweek of year:', dt.strftime(now, '%Y-%V'))
    res = datetime.date(now.year, now.month, now.day).isocalendar()
    print('week of year:', res[1])


def py_demo_delta_date():
    target_ts = dt.strptime('20210823', '%Y%m%d')
    cur_ts = dt.now()
    delta = target_ts - cur_ts
    print('\ndelta days:', delta.days)

    test_ts = dt.strptime('20210816', '%Y%m%d')
    delta = test_ts - target_ts
    print('delta days:', delta.days)


# regexp
#
# match:  返回匹配上的第一个字串。需要注意的是 match 函数是从字符串开始处开始查找的
# search: 函数类似于 match, 不同之处在于不限制正则表达式的开始匹配位置
#
# findall:  寻找所有匹配正则表达式的字串，返回一个列表
# finditer: findall 返回一个列表，finditer 返回一个迭代器

def py_demo_regexp_01():
    print(re.match('super', 'superstition').span())  # (0, 5)
    print(re.match('super', 'insuperable'))  # None

    print(re.search('super', 'superstition').span())  # (0, 5)
    print(re.search('super', 'insuperable').span())  # (2, 7)


def py_demo_regexp_02():
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


def py_demo_regexp_03():
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


# sort

def py_demo_sort_base():
    level_value_dict = {
        'na': 0,
        'low': 1,
        'mid': 2,
        'high': 3,
    }

    # 1: by lambda
    rows = ['low', 'high', 'low', 'high', 'mid', 'low', 'na', 'mid']
    sorted_rows = sorted(
        rows, key=lambda item: level_value_dict[item], reverse=True)
    print('result:', ','.join(sorted_rows))

    # 2: by custom compare func
    def mycmp(x, y):
        x_value = level_value_dict[x]
        y_value = level_value_dict[y]
        return y_value - x_value

    new_key = functools.cmp_to_key(mycmp)
    result = sorted(rows, key=new_key)
    print('result:', ','.join(result))


def py_demo_sort_objects():
    class student(object):
        def __init__(self, req_type: str, req_path: str, count: int):
            self.req_type = req_type
            self.req_path = req_path
            self.count = count

    def student_cmp(x: student, y: student) -> int:
        if x.req_type != y.req_type:
            return 1 if x.req_type > y.req_type else -1
        if x.req_path != y.req_path:
            return 1 if x.req_path > y.req_path else -1
        return y.count - x.count

    students = [
        student('http', '/xy', 97),
        student('rpc', '/foo', 176),
        student('http', '/ab/2', 63),
        student('http', '/xy', 275),
        student('rpc', '/bar', 81),
        student('http', '/cd', 491),
        student('http', '/xy', 55),
        student('http', '/ab/1', 29),
    ]
    cmp_key = functools.cmp_to_key(student_cmp)
    results = sorted(students, key=cmp_key)
    for s in results:
        print(s.req_type, s.req_path, s.count)


def py_demo_2levels_sort():
    # 1: string sort
    l = ['cn', 'id', 'es', 'cn', 'fr', 'es', 'cn']
    print(sorted(l, key=lambda item: item))

    def str_cmp(x, y) -> int:
        length = min(len(x), len(y))
        for idx in range(0, length):
            x_val = ord(x[idx])
            y_val = ord(y[idx])
            if x_val != y_val:
                return x_val - y_val
        return len(x) - len(y)

    result = sorted(l, key=functools.cmp_to_key(str_cmp))
    print(result)
    print()

    # 2: two levels sort: string => list of str
    class product(object):
        def __init__(self, category, regions, price):
            self.category = category
            self.regions = sorted(regions, key=lambda item: item)
            self.price = price

        def __str__(self):
            return f'type={self.category},region={"|".join(self.regions)},price={self.price}'

    products = [
        product('type_a', ['cn', 'en'], 99),
        product('type_b', ['es', 'fr'], 90),
        product('type_a', ['id', 'in'], 92),
        product('type_a', ['en', 'cn'], 101),
        product('type_b', ['br', 'mx'], 97),
        product('type_b', ['fr', 'es'], 95),
        product('type_a', ['cn', 'en'], 105),
        product('type_c', ['en', 'es'], 91),
        product('type_a', ['in', 'id'], 95),
    ]

    def my_comp(x, y) -> int:
        if x.category != y.category:
            return str_cmp(x.category, y.category)
        return str_cmp(','.join(y.regions), ','.join(x.regions))

    new_key = functools.cmp_to_key(my_comp)
    new_products = sorted(products, key=new_key)

    for product in new_products:
        print(product)


# dataclass

def py_demo_dataclass_base():
    # nest dataclass
    @dataclass
    class Player:
        name: str
        number: int
        position: str
        age: int

    @dataclass
    class Team:
        name: str
        players: List[Player]

    james = Player('Lebron James', 23, 'SF', 25)
    davis = Player('Anthony Davis', 3, 'PF', 21)
    lal = Team('Los Angeles Lakers', [james, davis])
    print(f'team: {lal.name}, players: {lal.players}')
    print()

    # immutable object
    @dataclass(frozen=True)
    class Data:
        name: str
        value: int = 42

    data = Data('foo', 31)
    # dataclasses.FrozenInstanceError: cannot assign to field 'name'
    # data.name = 'bar'
    print(f'data: {data}')


def py_demo_dataclass_field():
    # list 是一个可变默认值，使用默认工厂进行更改
    @dataclass
    class MyClazz:
        values: List[int] = field(default_factory=list)

    c = MyClazz()
    c.values += [1, 2, 3]
    print(f'one={c.values[0]}, two={c.values[1]}')

    # __post_init__ 方法
    @dataclass
    class MyClazz2:
        a: float
        b: float
        c: float = field(init=False)

        def __post_init__(self):
            self.c = self.a + self.b

    c2 = MyClazz2(10, 20)
    print(f'clazz: {c2}')


# reflect by inspect

def py_demo_fn_inspect():
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


def py_demo_object_inspect():
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


# importlib

def py_demo_import_mod():
    # pylint: disable=W4901,W4902
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
    # import imp
    # mod = imp.load_source('test_import_mod', file_path)
    # print(type(mod))
    # printTestClass(mod)
    # printTestMethod(mod.TestPy01)


def py_load_mod_and_run():
    # pylint: disable=W4902
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
    with open(file_path, mode='w', encoding='utf8') as f:
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


# bits state

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


def py_demo_bits_state_01():
    print('\nall operations: create=%s, write=%s, remove=%s, rename=%s'
          % (bin(Operation.Create), bin(Operation.Write), bin(Operation.Remove), bin(Operation.Rename)))
    op = Operation()
    op.value = Operation.Create
    op.value = Operation.Remove
    op.value = Operation.Rename
    print('has create:', op.has_create())
    print('has write:', op.has_wirte())
    print('cur op:', op)


def py_demo_bits_state_02():
    state_qa = 1
    state_dev = 1 << 1
    state_pm = 1 << 2

    l = ['qa, pm', 'dev', 'dev, qa']
    for data in l:
        cur_state = 0
        if 'qa' in data:
            cur_state += state_qa
        if 'dev' in data:
            cur_state += state_dev
        if 'pm' in data:
            cur_state += state_pm

        result = []
        if cur_state & state_qa != 0:
            result.append('qa')
        if cur_state & state_dev != 0:
            result.append('dev')
        if cur_state & state_pm != 0:
            result.append('pm')
        print('|'.join(result))


# pipeline

def py_demo_pipe_01():
    nums =[1, 2, 3, 4, 5, 6]
    nums = filter(lambda x: x % 2 == 0, nums)
    nums = map(lambda x: x ** 2, nums)
    print('results:', list(nums))


def py_demo_pipe_02():
    from pipe import select, where

    nums =[1, 2, 3, 4, 5, 6]
    # pylint: disable=E1120
    result = list(nums | where(lambda x: x % 2 == 0) | select(lambda x: x ** 2))
    print('results:', result)


# py exp


def py_demo_exp_01():
    # 推导式
    numbers = [1, 2, 3, -3, -2, -1]
    my_list = [x*x for x in numbers]
    print(my_list)
    my_dict = {x: pow(10, x) for x in numbers}
    print(my_dict)
    my_set = {abs(x) for x in numbers}
    print(my_set)
    print()

    # Counter
    data = [1, 1, 1, 1, 2, 3, 4, 3, 3, 5, 6, 7, 7]
    count = Counter(data)
    for k, v in count.items():
        print(f'{k}={v}')
    print()

    # namedtuple
    Direction = namedtuple('Direction', 'N,S,E,W')
    di = Direction(4, 74, 0, 0)
    print(di)
    print()

    # OrderedDict
    d = OrderedDict()
    d['a'] = 5
    d['d'] = 2
    d['c'] = 1
    d['b'] = 3
    print(d)

    # defaultdict
    dd = defaultdict(int)
    dd['a'] = 2
    print(dd['a'])
    print(dd['b'])  # 0


def py_demo_exp_02():
    # title
    print('samuel colvin'.title())
    print()

    # str compare
    print('a > b:', 'a' > 'b')
    print('aa > ab:', 'aa' > 'ab')
    print('abc > abd:', 'abc' > 'abd')
    print()

    # 泰文 bytes 转 str
    s = b'\340\271\204\340\270\241\340\271\210\340\270\252\340\270\262\340\270\241\340\270\262\340\270\243\340\270\226\340\271\203\340\270\212\340\271\211\340\270\204\340\270\271\340\270\233\340\270\255\340\270\207\340\270\231\340\270\265\340\271\211'
    if isinstance(s, bytes):
        print('bytes decode:', s.decode())
    else:
        print('string:', s)
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
    print()

    # 修改列表的元素值
    lst = 'a|b|c|d|e|f|g'.split('|')
    for val in lst:
        val = val + 'x'
    print('unchange:', lst)

    new_lst = [val + 'x' for val in lst]
    print('change:', new_lst)


def py_demo_run_stack():
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


if __name__ == '__main__':

    try:
        # py_demo_if_cond()
        # py_demo_pipe_02()
        py_demo_calculate()
    except:
        traceback.print_exc()

    print('py base demo ext DONE.')
