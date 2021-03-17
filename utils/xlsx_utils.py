# -*- coding: utf-8 -*-
'''
Created on 2019-03-07

@author: zhengjin
'''

import os
import json
import sys
import xlrd

sys.path.append(os.getenv('PYPATH'))
from utils import Constants
from utils import LogManager


class XlsxUtils(object):

    __xlsx = None

    @classmethod
    def get_instance(cls):
        if cls.__xlsx is None:
            cls.__xlsx = XlsxUtils()
        return cls.__xlsx

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__sheet = None

    def get_all_sheets_names(self, file_path):
        self.__verify_target_file(file_path)

        workbook = xlrd.open_workbook(file_path)
        ret_names = []
        for sheet in workbook.sheets():
            ret_names.append(sheet.name)
        return ret_names

    def __verify_target_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError('Target file is not exist: ' + file_path)
        if not os.path.isfile(file_path):
            raise IOError('Target file is not type file: ' + file_path)

    # --------------------------------------------------------------
    # Read excel data for one sheet
    # --------------------------------------------------------------
    def pre_read_sheet(self, file_path, sheet_name):
        self.__verify_target_file(file_path)

        self.__logger.info('load data from excel / sheet: %s / %s' % (file_path, sheet_name))
        workbook = xlrd.open_workbook(file_path)
        self.__sheet = workbook.sheet_by_name(sheet_name)
        return self

    def read_header_row(self):
        self.__verify_before_read_data()
        ret_header = []
        for cell in self.__sheet.get_rows().__next__():
            ret_header.append(cell.value)

        return ret_header

    def read_all_rows_by_sheet(self, is_include_header=False):
        self.__verify_before_read_data()
        ret_rows = []
        for row in self.__sheet.get_rows():
            tmp_row = []
            for cell in row:
                tmp_row.append(str(cell.value))
            ret_rows.append(tmp_row)

        return ret_rows[1:] if is_include_header else ret_rows

    def read_values_by_cloumn(self, col_num, is_include_header=False):
        self.__verify_before_read_data()
        ret_vals = []
        for row in self.__sheet.get_rows():
            ret_vals.append(row[col_num].value)

        return ret_vals[1:] if is_include_header else ret_vals

    def read_cell_value(self, row_num, col_num):
        self.__verify_before_read_data()
        ret_val = self.__sheet.cell(row_num, col_num).value
        return str(ret_val)

    def __verify_before_read_data(self):
        if self.__sheet is None:
            raise Exception('Pls load sheet data first!')

    # --------------------------------------------------------------
    # Write data to excel sheet
    # --------------------------------------------------------------
    # TODO:


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    xlsx = XlsxUtils.get_instance()

    sheet_name = 'Module01'
    file_path = os.path.join(os.getenv('PYPATH'), 'apitest/TestCases.xlsx')
    print(xlsx.get_all_sheets_names(file_path))

    xlsx.pre_read_sheet(file_path, sheet_name)
    print(xlsx.read_header_row())

    # excel cell index start with (0,0)
    # print('1st case name:', xlsx.read_cell_value(1, 1))
    # print('test cases:', xlsx.read_values_by_cloumn(1))
    print(xlsx.read_all_rows_by_sheet())

    LogManager.clear_log_handles()
    print('xlsx utils test DONE.')
