# -*- coding: utf-8 -*-
'''
Created on 2019-03-11
@author: zhengjin

Define test setup and tearup functions bind with pytest fixtures ("session" and "module" scope).
'''

import os
import sys
import allure
import pytest

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.path.index(project_dir)
except ValueError:
    sys.path.append(project_dir)

from utils import Constants
from utils import LogManager
from utils import SysUtils
Constants.add_project_paths()

from common import LoadConfigs
from common import LoadCases


project_path = os.path.join(os.getenv('PYPATH'), 'apitest')


def load_configs():
    cfg_file_path = os.path.join(project_path, 'configs.ini')
    LoadConfigs.load_configs(cfg_file_path)


def init_logger():
    logdir_path = LoadConfigs.get_testenv_configs().get('logdir_path')
    logdir_path = logdir_path.replace('{project}', project_path)
    logfile_path = os.path.join(
        logdir_path, 'pytest_log_%s.txt' % SysUtils.get_current_date_and_time())
    LogManager.build_logger(logfile_path)


def load_testcases():
    tc_file_path = LoadConfigs.get_testenv_configs().get('tc_file_path')
    tc_file_path = tc_file_path.replace('{project}', project_path)
    LoadCases.get_instance().load_all_cases(tc_file_path)


def init_allure_env():
    allure.environment(report='Allure report', browser='Firefox', hostname='zhengjin.host.local')


@pytest.fixture(scope='session')
def setup_test_session(request):
    '''
    Setup for test session: 
    1) init logger and allure; 2) load configs and testcases.
    '''
    load_configs()
    init_logger()
    load_testcases()
    init_allure_env()

    logger = LogManager.get_logger()
    logger.info('[session setup]: 1) init logger and allure; 2) load configs and testcases.')

    def clear():
        logger.info('[session clearup] done.')
        LogManager.clear_log_handles()
    request.addfinalizer(clear)


if __name__ == '__main__':

    isTest = True
    if isTest:
        print(sys.path)
        print('Done')
    else:
        # load_configs()
        init_logger()
        load_testcases()

        tcs = LoadCases.get_instance().get_loaded_tcs()
        LogManager.get_logger().info(tcs)
        LogManager.get_logger().info('conftest DONE.')
        LogManager.clear_log_handles()
