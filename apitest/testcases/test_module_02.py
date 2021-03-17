# -*- coding: utf-8 -*-
'''
Created on 2019-03-10
@author: zhengjin
'''

import logging
import sys
import os
import allure
import pytest

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.path.index(project_dir)
except ValueError:
    sys.path.append(project_dir)

from utils import Constants
from utils import LogManager
from utils import HttpUtils
Constants.add_project_paths()

from common import LoadCases
from testcases import TestBase


@allure.feature('MockTest')
@allure.story('Story_RetCodePage')
class TestModule02(TestBase):

    __logger = None
    __http_utils = None

    def setup_class(cls):
        cls.__logger = LogManager.get_logger()
        cls.__http_utils = HttpUtils.get_instance()

    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.__cur_case = method.__name__

    def teardown_method(self, method):
        pass

    def test_error_get_01(self):
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case[self.CASE_SCHEMA_HEADER])
        resp = self.__http_utils.send_http_request(
            case[self.CASE_SCHEMA_METHOD], case[self.CASE_SCHEMA_URL], 
            case[self.CASE_SCHEMA_QUERY], headers=headers)
        self.base_http_assert(resp)

    @pytest.allure.severity(pytest.allure.severity_level.MINOR)
    def test_error_get_02(self):
        allure.attach('error code desc', 'verify api returned code 206.')
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case[self.CASE_SCHEMA_HEADER])
        resp = self.__http_utils.send_http_request(
            case[self.CASE_SCHEMA_METHOD], case[self.CASE_SCHEMA_URL], 
            case[self.CASE_SCHEMA_QUERY], headers=headers)
        self.base_http_assert(resp, 206)

    @pytest.allure.severity(pytest.allure.severity_level.MINOR)
    def test_error_get_03(self):
        allure.attach('error code desc', 'verify api returned code 400.')
        case = LoadCases.get_instance().get_tc_data_dict(self.__cur_case)
        headers = LoadCases.format_headers_to_dict(case[self.CASE_SCHEMA_HEADER])
        resp = self.__http_utils.send_http_request(
            case[self.CASE_SCHEMA_METHOD], case[self.CASE_SCHEMA_URL], 
            case[self.CASE_SCHEMA_QUERY], headers=headers)
        self.base_http_assert(resp, 400)


if __name__ == '__main__':

    isTest = True
    if isTest:
        print('Done')
    else:
        LogManager.build_logger(Constants.LOG_FILE_PATH, stream_log_level=logging.DEBUG)
        file_path = os.path.join(os.path.dirname(os.getcwd()), 'TestCases.xlsx')
        LoadCases.get_instance().pre_load_sheet(file_path, 'Module02').load_all_cases_by_sheet()

        pytest.main(['-v', '-s', 'test_module_02.py'])

        LogManager.clear_log_handles()
        print('test module 02 DONE.')
