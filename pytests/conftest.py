# -*- coding: utf-8 -*-
'''
Created on 2019-03-10
@author: zhengjin
'''

import allure
import pytest


@pytest.fixture
# @pytest.fixture(scope='function')
def ft_hook_case():
    '''
    run before and after each test case.
    '''
    printWithPrefix('[fixture_hook_case] before invoked.')
    yield 0
    printWithPrefix('[fixture_hook_case] after invoked.')


@pytest.fixture(scope='class')
def ft_hook_class():
    '''
    run before and after each test class.
    '''
    printWithPrefix('[fixture_hook_class] before invoked.')
    yield 0
    printWithPrefix('[fixture_hook_class] after invoked.')


@pytest.fixture(scope='module')
def ft_hook_module(request):
    '''
    run before and after py module.
    '''
    printWithPrefix('[fixture_hook_module] before invoked.')

    def clear():
        printWithPrefix('[fixture_hook_module] after invoked.')
    request.addfinalizer(clear)
    return 0


@pytest.fixture(scope='session')
def ft_hook_session(request):
    '''
    run before and after test session.
    '''
    printWithPrefix('[fixture_hook_session] before invoked.')

    def clear():
        printWithPrefix('[fixture_hook_session] after invoked.')
    request.addfinalizer(clear)
    return 0


@pytest.fixture(scope='module')
def ft_lang_data():
    '''
    return lang data with module scope.
    '''
    printWithPrefix('[fixture_lang_data] init.')
    common_data = {
        'language': ['python', 'java', 'golang', 'javascript', 'c++']
    }
    yield common_data
    printWithPrefix('[fixture_lang_data] tearup.')


@pytest.fixture(params=['smtp.gmail.com', 'mail.python.org'])
def ft_mails_data(request):
    '''
    return each mail item with case scope.
    '''
    printWithPrefix('[fixture_mails_data] init.')
    mail_addr = request.param

    def clear():
        printWithPrefix('[fixture_mails_data] finalizing %s' % mail_addr)
    request.addfinalizer(clear)
    return mail_addr


@pytest.fixture(scope='session')
def init_allure_env():
    printWithPrefix('[init_allure_env] invoked.')
    allure.environment(report='Allure report', hostname='zhengjin.host.local')


def printWithPrefix(text):
    print('\n======', text)
