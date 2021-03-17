# -*- coding: utf-8 -*-
'''
Created on 2019-03-12
@author: zhengjin
'''

import allure
import pytest


@pytest.mark.usefixtures('ft_hook_module', 'ft_hook_session')
@pytest.mark.usefixtures('init_allure_env')
class TestPyFixturesBase(object):

    def test_fixture_base_01(self):
        allure.attach('base test desc', '\n'.join([
            '1) test fixtures [module] and [session] scope across .py modules;',
            '2) invoke [init_allure_env] fixture.',
        ]))
        print('\n[test_fixture_base_01] is running ...')
        assert(True)

    def test_fixture_base_02(self):
        pass


if __name__ == '__main__':

    pytest.main(['-v', '-s', 'test_pytest_base.py'])
