# -*- coding: utf-8 -*-
'''
Created on 2019-01-13
@author: zhengjin

Run test demos by using "pytest" module.

pytest commands:
$ py.test -h
$ py.test --version

pytest plugins:
pytest-html
pytest-rerunfailures

Refer: 
http://pythontesting.net/framework/pytest/pytest-introduction/
'''

import allure
import pytest


def print_prefix(text):
    print('\n======>', text)


def setup_module(module):
    print_prefix('[setup_module] module:%s' % module.__name__)


def teardown_module(module):
    print_prefix('[teardown_module] module:%s' % module.__name__)


@allure.feature('FeaturePyTest')
@allure.story('PyTestStory01')
class TestPyDemo01(object):

    def setup_class(cls):
        print_prefix('[setup_class] class:%s' % cls.__name__)

    def teardown_class(cls):
        print_prefix('[teardown_class] class:%s' % cls.__name__)

    def setup_method(self, method):
        print_prefix('[setup_method] method:%s' % method.__name__)

    def teardown_method(self, method):
        print_prefix('[teardown_method] method:%s' % method.__name__)

    def setup(self):
        print_prefix('[setup] method: n/a')

    def teardown(self):
        print_prefix('[teardown] method: n/a')

    @pytest.allure.severity(pytest.allure.severity_level.MINOR)
    def test_numbers_5_6(self):
        allure.attach('my attach', 'pytest allure attach test.')
        print_prefix('[test_numbers_5_6]')
        assert((5 * 6) == 30)

    @pytest.allure.severity(pytest.allure.severity_level.MINOR)
    def test_strings_b_2(self):
        print_prefix('[test_strings_b_2]')
        assert((2 * 'x') == 'xx')

    # @pytest.mark.skip(reason='no run')
    @pytest.mark.timeout(2)
    def test_random_num_timeout(self):
        import time
        time.sleep(1)
        import random
        assert(random.randint(0, 5) > 2)

    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    def test_random_choice_rerun(self):
        import random
        assert(random.choice([True, False]))

    testdata = [(5, 6, 30), (2, 10, 20), ]

    @pytest.mark.parametrize('a,b,expected', testdata)
    def test_number_a_b(self, a, b, expected):
        print_prefix('[test_numbers_a_b]')
        assert((a * b) == expected)
# TestPyDemo01 end


# @pytest.mark.skip(reason='no run')
@allure.feature('FeatureMyTest')
@allure.story('PyTestStory02')
class TestPyDemo02(object):

    def test_01_collections_deque(self):
        names = ['jack', 'leo', 'sam', 'peter', 'jeo']

        import collections
        deque_names = collections.deque(names)
        deque_names.popleft()
        deque_names.appendleft('mark')
        print(deque_names)

    def test_02_dict_get_default(self):
        colors = ['red', 'green', 'red', 'blue', 'green', 'red']

        with pytest.allure.step('dict get default step1'):
            tmp_dict01 = {}
            for color in colors:
                tmp_dict01.setdefault(color, 0)
                tmp_dict01[color] += 1
            print(tmp_dict01)

        with pytest.allure.step('dict get default step2'):
            tmp_dict02 = {}
            for color in colors:
                tmp_dict02[color] = tmp_dict02.get(color, 0) + 1
            print(tmp_dict02)

    def test_03_default_dict(self):
        names = ['jack', 'leo', 'sam', 'peter', 'jeo']

        from collections import defaultdict
        tmp_dict = defaultdict(list)
        for name in names:
            key = len(name)
            tmp_dict[key].append(name)
        print(tmp_dict)
# TestPyDemo02 end


if __name__ == '__main__':

    pytest.main(['-v', '-s', 'test_pytest.py'])

    # if specify class, setup_module() and teardown_module() not trigger
    # pytest.main(['-v', '-s', 'py_test02.py::TestPyBase'])
