# coding=utf-8

import keyword
import importlib
import inspect
import os

# vars() => __dict__


def is_test_case(method):
    return hasattr(method, 'desc')


def get_testcases_from_class(clazz) -> list:
    methods = [val for _, val in vars(clazz).items(
    ) if inspect.isfunction(val) and is_test_case(val)]
    return methods


def load_class_from_py_file(file_name) -> list:
    file_path = os.path.abspath(file_name)
    mod_name = os.path.splitext(file_name)[0]

    source = importlib.machinery.SourceFileLoader(mod_name, file_path)
    mod = source.load_module(mod_name)
    clazz = [val for _, val in vars(mod).items() if inspect.isclass(val)]
    return clazz


def main_class_parse():
    clazz = load_class_from_py_file('test_class.py')
    for c in clazz:
        print('test suite:', c.__name__)
        instance = c()
        for t in get_testcases_from_class(c):
            print('found test case: name=%s, desc=%s' % (t.__name__, t.desc))
            t(instance)
        print()


if __name__ == '__main__':

    main_class_parse()
