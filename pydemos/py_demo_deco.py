# coding=utf-8
# pylint: disable=C0104,W0718

import functools
import glob
import os
from typing import Any, Callable

# deco: wrap(deco_params) => deco(func) => inner_deco(func_params)


def py_demo_deco_base_01():
    def wrap(author='bar'):
        def _deco(func):
            setattr(func, 'author', author)  # add a attribute

            @functools.wraps(func)
            def _inner_deco(*args):
                print('\npre-hook')  # add hooks
                ret = func(*args)
                print('after-hook')
                return ret
            return _inner_deco

        return _deco

    @wrap(author='jin.zheng')
    def say_hello(name: str):
        return 'hello ' + name

    # exec deco wrap() before
    assert hasattr(say_hello, 'author')
    print(f'func={say_hello.__name__}, author={say_hello.author}')
    print(say_hello('foo'))


def py_demo_deco_base_02():
    # 1
    def deco_without_params(fn):
        def _deco(*arg):
            fn.is_test = True
            print('deco: deco_without_params')
            return fn(*arg)
        return _deco

    @deco_without_params
    def a(name):
        return 'fn:a hello: ' + name

    print(a('foo'))
    print(hasattr(a, 'is_test'))
    print()

    # 2
    def deco_with_params():
        def _deco(fn):
            print('deco: deco_with_params')

            def _inner_deco(*arg):
                setattr(fn, 'is_test', True)
                print('deco: deco_with_params inner')
                return fn(*arg)
            return _inner_deco
        return _deco

    @deco_with_params()
    def b(name):
        return 'fn:b hello: ' + name

    print(b('bar'))
    print(hasattr(b, 'is_test'))
    print()

    # 3
    def deco_for_add_attr():
        def _deco(fn):
            print('deco: deco_for_add_attr')
            fn.is_test = True
            return fn
        return _deco

    @deco_for_add_attr()
    def c(name):
        return 'fn:c hello: ' + name

    print(hasattr(c, 'is_test'))
    # print(c('jim'))


# Decorator for class function

def py_demo_deco_for_class():
    def verify_dir_path(func):
        def _deco(*args, **kwargs):
            this = args[0]
            print('verify dir path:', this.dir_path)
            if not os.path.exists(this.dir_path):
                raise FileNotFoundError('dir path is not exist!')
            if not os.path.isdir(this.dir_path):
                raise IOError('dir path is not invalid!')
            return func(*args, **kwargs)

        return _deco

    class ListFile(object):
        def __init__(self, dir_path):
            self.dir_path = dir_path

        @verify_dir_path
        def listTextFiles(self):
            files = glob.glob(self.dir_path + '/*.txt')
            print('text files:', files)

        @verify_dir_path
        def listYmlFiles(self):
            files = glob.glob(self.dir_path + '/*.yml')
            print('yml files:', files)

    list_file = ListFile(os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files'))
    list_file.listTextFiles()
    list_file.listYmlFiles()


# 类装饰器

def py_demo_class_deco_01():
    class TargetFn:
        def __init__(self, fn: Callable) -> None:
            self._fn = fn

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            print('deco: TargetFn')
            return self._fn(*args, **kwargs)

    check = TargetFn

    @check
    def a():
        print('fn:a')

    print(type(a), isinstance(a, Callable))
    a()


def py_demo_class_deco_02():
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

    @MyLogging(level='warn')  # 执行 __call__ 方法
    def bar(a, b):
        print('i am bar: %d' % (a+b))

    print(type(bar))
    bar(1, 2)


if __name__ == '__main__':

    # py_demo_deco_base_01()
    # py_demo_deco_base_02()

    # try:
    #     py_demo_deco_for_class()
    # except Exception as e:
    #     print('error:', e)

    py_demo_class_deco_01()
    # py_demo_class_deco_02()

    print('py deco done')
