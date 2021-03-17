# -*- coding: utf-8 -*-
'''
Created on 2019-03-30
@author: zhengjin
'''

import pytest


@pytest.mark.usefixtures('ft_hook_case', 'ft_hook_class')
@pytest.mark.usefixtures('ft_hook_module', 'ft_hook_session')
class TestPyFixtures01(object):

    def test_fixture_011(self):
        print('\n[test_fixture_011] is running ...')
        assert(True)

    def test_fixture_012(self):
        print('\n[test_fixture_012] is running ...')
        assert(True)
# TestPyFixtures01 end


@pytest.mark.usefixtures('ft_hook_case', 'ft_hook_class')
@pytest.mark.usefixtures('ft_hook_module', 'ft_hook_session')
class TestPyFixtures02(object):

    def test_fixture_021(self):
        print('\n[test_fixture_021] is running ...')
        assert(True)
# TestPyFixtures02 end


class TestPyFixtures03(object):

    def test_fixture_031(self, ft_lang_data):
        lang = ft_lang_data['language']
        print('\n[test_fixture_031] lang:', lang)
        assert(len(lang) == 5)

    def test_fixture_032(self, ft_lang_data):
        lang = ft_lang_data['language']
        print('\n[test_fixture_032] lang:', lang)
        assert(len(lang) == 5)

    def test_fixture_033(self, ft_mails_data):
        print('\n[test_fixture_033] mail addr:', ft_mails_data)
        assert(True)
# TestPyFixtures03 end


class TestPyFixtures04(object):

    @pytest.fixture
    def ft_fruit_data(self, request):
        print('\n[fixture_fruit_data] init fruit.')
        names = ['apple', 'banana', 'pair', 'orange']

        def clear():
            print('\n[fixture_fruit_data] finalizing fruit.')
        request.addfinalizer(clear)
        return names

    def test_fixture_041(self, ft_fruit_data):
        print('\n[test_fixture_041] names:')
        for name in ft_fruit_data:
            print(name)
        assert(True)

    def test_fixture_042(self, ft_fruit_data):
        print('\n[test_fixture_042] names:', ft_fruit_data)
        assert(True)
# TestPyFixtures04 end


if __name__ == '__main__':

    pytest.main(['-v', '-s', 'test_pytest_fixtures.py'])
