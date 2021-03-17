# coding: utf-8

import os
import sys
import importlib
import inspect

from my_annotations import TestMeta


def run_tests():
    # classes = load_test_classes()
    classes = load_classes_from_source('my_tests.py')
    for clazz in classes:
        _self = clazz()
        for test in getattr(clazz, 'tests'):
            if run_tests_cond_priority(test.test_meta, 1):
                print(
                    f"Run Test: meta:{test.test_meta.to_string()}, desc:{test.test_desc}")
                test(_self)


def load_test_classes():
    import my_tests

    ret = []
    for s in (my_tests.MyTestSuite01, my_tests.MyTestSuite02, my_tests.MyTestSuite03):
        if hasattr(s, 'tests'):
            ret.append(s)
        else:
            print(f"[{s.__name__}]: No tests found!")
    return ret


def load_classes_from_source(file_name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(cur_dir, file_name)
    full_name = os.path.splitext(file_name)[0]
    source = importlib.machinery.SourceFileLoader(full_name, file_path)
    imported = source.load_module(full_name)

    ret = []
    for _, value in vars(imported).items():
        if inspect.isclass(value) and 'testsuite' in value.__name__.lower():
            if hasattr(value, 'tests'):
                ret.append(value)
            else:
                print(f"[{value.__name__}]: No tests found!")
    return ret


def run_tests_cond_priority(test: TestMeta, pri: int):
    return test.priorityNumber <= pri


if __name__ == '__main__':

    run_tests()
    print('run test demo Done.')
