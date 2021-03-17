# coding: utf-8

from typing import List, Callable
from my_annotations import test_meta, test_desc, TestMeta

"""
MetaClass:

1. __new__ 是在生成类之前通过修改其属性列表 dic 的方式来控制类的创建，此时类还没有被创建
2. __init__ 是在 __new__ 函数返回被创建的类之后，通过直接增删类的属性的方式来修改类，此时类已经被创建
3. __new__ 函数的第一个参数 typ 代表的是元类 MyMetaClass（注意不是元类的对象）
4. __init__ 函数的第一个参数 cls 表示的是类 MyTestSuite, 也就是元类 MyMetaClass 的一个实例（对象）
"""


class MyMetaClass01(type):
    """ metaclass __new__ """

    def __new__(typ, classname, bases, class_dict):
        tests: List[Callable] = [item for item in class_dict.values(
        ) if callable(item) and hasattr(item, 'test_meta')]
        if len(tests) > 0:
            print(classname, 'inject tests:', [t.__name__ for t in tests])
            class_dict['tests'] = tests

        return type.__new__(typ, classname, bases, class_dict)


class MyTestBase01(metaclass=MyMetaClass01):

    def __init__(self):
        pass


class MyTestSuite01(MyTestBase01):

    @test_desc('test case 01, foo')
    @test_meta(TestMeta(title='case01', priority=1))
    def testCase01(self):
        print('This is test case 01, say foo')

    @test_desc('test case 02, bar')
    @test_meta(TestMeta(title='case02', priority=2))
    def testCase02(self):
        print('This is test case 02, say bar')


class MyMetaClass02(type):
    """ metaclass __init__ """

    def __init__(mcs, classname, bases, class_dict):
        tests: List[Callable] = [item for item in vars(
            mcs).values() if callable(item) and hasattr(item, 'test_meta')]
        if len(tests) > 0:
            print(classname, 'inject tests:', [t.__name__ for t in tests])
            assert not hasattr(mcs, 'tests')
            setattr(mcs, 'tests', tests)


class MyTestBase02(metaclass=MyMetaClass02):

    def __init__(self):
        pass


class MyTestSuite02(MyTestBase02):

    @test_desc('test case 11, foo')
    @test_meta(TestMeta(title='case11', priority=1))
    def testCase11(self):
        print('This is test case 11, say foo')

    @test_desc('test case 12, bar')
    @test_meta(TestMeta(title='case12', priority=2))
    def testCase12(self):
        print('This is test case 12, say bar')

    def testCase13(self):
        print('This is test case 13, hello')


class MyTestSuite03(MyTestBase02):

    def __init__(self):
        pass


if __name__ == '__main__':

    import inspect
    print('get test funcs in class by inspect:')
    for clazz in (MyTestSuite01, MyTestSuite02):
        tests = {name: func for name, func in inspect.getmembers(
            clazz, inspect.isfunction) if hasattr(func, 'test_meta')}
        print(f"[{clazz.__name__}] includes test cases: {list(tests.keys())}")

    print('\nget test funcs in class by vars():')
    for clazz in (MyTestSuite01, MyTestSuite02):
        tests = {name: func for name, func in vars(
            clazz).items() if callable(func) and hasattr(func, 'test_meta')}
        print(f"[{clazz.__name__}] includes test cases: {list(tests.keys())}")
