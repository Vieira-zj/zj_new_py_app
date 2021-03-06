# coding=utf-8

import keyword
import importlib
import inspect
import os

# vars() => __dict__


def load_class_from_py_file(file_name) -> list:
    file_path = os.path.abspath(file_name)
    mod_name = os.path.splitext(file_name)[0]
    print(f'start load: file={file_path},module={mod_name}')

    source = importlib.machinery.SourceFileLoader(mod_name, file_path)
    mod = source.load_module(mod_name)
    print(f'end load: file={file_path},module={mod_name}')

    clazz = [val for _, val in vars(mod).items() if inspect.isclass(val)]
    return clazz


def get_testcases_from_class(clazz) -> list:
    methods = [val for _, val in vars(clazz).items(
    ) if inspect.isfunction(val) and is_test_case(val)]
    return methods


def is_test_case(method):
    return hasattr(method, 'desc')

# main


def main_class_parse():
    # run deco of func when load module
    clazz = load_class_from_py_file('test_class.py')
    for c in clazz:
        print('\ntest suite:', c.__name__)
        instance = c()
        for t in get_testcases_from_class(c):
            print('found test case: name=%s,desc=[%s]' % (t.__name__, t.desc))
            t(instance)


if __name__ == '__main__':

    main_class_parse()
