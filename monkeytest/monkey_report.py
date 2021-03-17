'''
Created on 2018-11-26

@author: zhengjin
'''

import re
import os
import sys

sys.path.append(os.getenv('PYPATH'))
from utils import Constants, LogManager, SysUtils


class MonkeyReport(object):
    '''
    classdocs
    '''

    def __init__(self, log_root_dir_path, log_exception_name, log_anr_name):
        '''
        Constructor
        '''
        self.__log_exception_path = os.path.join(
            log_root_dir_path, log_exception_name)
        self.__log_anr_path = os.path.join(log_root_dir_path, log_anr_name)
        self.__monkey_test_report_path_for_win = os.path.join(
            log_root_dir_path, 'monkey_test_report.txt')

        self.__logger = LogManager.get_logger()
        self.__sysutils = SysUtils()

    # --------------------------------------------------------------
    # Create report
    # --------------------------------------------------------------
    def create_monkey_test_report(self, dict_title):
        '''
        Include: package name, run time, device info, app info, exception sum info, total anr
        '''
        output_lines = []
        output_lines = output_lines + ['%s: %s\n' % (k, v) for k, v in dict_title.items()]

        output_lines.append('\nAPP exceptions summary info:\n')
        output_lines = output_lines + self.__get_exception_sum_info()

        output_lines.append('\rAPP ANR summary info:\n')
        output_lines.append('Total ANR: %d\n' % self.__get_anr_sum_info())

        self.__sysutils.write_lines_to_file(
            self.__monkey_test_report_path_for_win, output_lines)

    def __get_exception_sum_info(self):
        input_lines = self.__sysutils.read_lines_from_file(self.__log_exception_path)

        ret_dict = {}
        exception_key = ''
        for line in input_lines:
            if 'W System.err' not in line:
                continue

            re_results = re.match('.+:\s+(.*Exception.{20,100})', line)
            try:
                exception_key = re_results.group(1)
            except AttributeError as e:
                continue

            try:
                ret_dict[exception_key] = ret_dict[exception_key] + 1
            except KeyError as e:
                ret_dict[exception_key] = 1
        # end for

        if len(ret_dict) == 0:
            return ['null\n']
        return ['total: %d, desc: %s\n' % (v, k) for k, v in ret_dict.items()]

    def __get_anr_sum_info(self):
        input_lines = self.__sysutils.read_lines_from_file(self.__log_anr_path)
        totals = 0

        for line in input_lines:
            if 'E ANRManager: ANR' in line:
                totals = totals + 1
        return totals


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)

    log_dir_path = r'D:\ZJWorkspaces\ZjPy3Project\monkeyreports\18-11-27_150443'
    report = MonkeyReport(log_dir_path, 'logcat_exception.log', 'logcat_anr.log')

    title_dict = {}
    title_dict['TEST PACKAGE'] = 'com.jd.b2b'
    title_dict['RUN TIME'] = '60'
    report.create_monkey_test_report(title_dict)

    LogManager.clear_log_handles()
    print('Monkey report DONE.')
