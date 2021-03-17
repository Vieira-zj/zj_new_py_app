# -*- coding: utf-8 -*-
'''
Created on 2019-01-18
@author: zhengjin

Read json body from excel, sent http post request and validate json repsonse.
libs: xlrd (excel read), xlwt (excel write)
'''

import json
import os
import sys
import xlrd
from urllib import parse, request

sys.path.append(os.getenv('PYPATH'))

from utils import Constants
from utils import LogManager


class ApiTestByExcel(object):

    def __init__(self, logger, file_path):
        if len(file_path) == 0:
            raise ValueError('input excel file path is null!')
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                'input excel file path is not exist: ' + file_path)

        self.__workbook = xlrd.open_workbook(file_path)
        self.__logger = logger

    def read_json_bodies_by_col(self, sheet_idx, col_num, start_idx=0, end_idx=0):
        sheets = self.__workbook.sheet_names()
        self.__logger.debug('excel sheet: ' + str(sheets))

        if sheet_idx >= len(sheets):
            raise ValueError('invalid sheet index:', sheet_idx)
        target_sheet = self.__workbook.sheet_by_index(sheet_idx)

        ret_bodies = []
        if end_idx == 0:
            end_idx = target_sheet.nrows
        for i in range(start_idx, end_idx):
            req_json_body = target_sheet.cell(i, col_num).value
            if req_json_body is None or len(req_json_body) == 0:
                self.__logger.debug(
                    'loop at %d, request body is null and skipped.' % i)
                ret_bodies.append('null')
            else:
                self.__logger.debug(
                    'loop at %d, request json body: %s' % (i, req_json_body))
                ret_bodies.append(req_json_body)

        return ret_bodies

    def http_post_req(self, url, req_json_body):
        header_dict = {'Content-Type': 'application/json'}
        req = request.Request(url=url, data=req_json_body, headers=header_dict)
        resp = request.urlopen(req)
        self.__logger.debug('resp code: %d' % resp.status)
        self.__logger.debug('resp headers:\n' + str(resp.headers))

        resp_body = resp.read().decode(Constants.CHARSET_UTF8)
        self.__logger.debug('resp body:\n' + resp_body)
        return resp_body


def excel_demo01():
    manager = LogManager(Constants.LOG_FILE_PATH)
    logger = manager.get_logger()

    # test read json bodies from excel
    file_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files/smoke_test.xlsx')
    api_test = ApiTestByExcel(logger, file_path)

    is_read_json_req_body = False
    if is_read_json_req_body:
        req_bodies = api_test.read_json_bodies_by_col(
            sheet_idx=1, col_num=5, start_idx=3, end_idx=6)
        for body in req_bodies:
            logger.debug('request json body: ' + body)

    is_read_json_resp_body = False
    if is_read_json_resp_body:
        expect_resp_bodies = api_test.read_json_bodies_by_col(
            sheet_idx=1, col_num=7, start_idx=3, end_idx=6)
        for body in expect_resp_bodies:
            logger.debug('expected response json body: ' + body)

    # test http post
    is_post_req = False
    if is_post_req:
        url = 'http://localhost:17891/index'
        req_json = {'key1': 'value1'}
        req_json_text = json.dumps(req_json).encode(
            encoding=Constants.CHARSET_UTF8)
        resp_json_body = api_test.http_post_req(url, req_json_text)

        # mock json response
        json_text = json.dumps({'status': 'OK', 'score': 0.91})
        resp_json_body = json.loads(json_text)
        logger.info('response results: status => %s, score => %s' %
                    (resp_json_body['status'], resp_json_body['score']))

    manager.clear_log_handles()


def read_all_data_excel():
    import pandas as pd

    file_path = os.path.join(os.getenv('HOME'), 'Downloads', 'test.xlsx')
    df = pd.read_excel(file_path, sheet_name='sheet1', header=0, index_col=0)
    print('dataframe:\n', df)
    print()

    rows_size = df.index.size
    cols_size = df.columns.size
    print('cols count=%d, rows count=%d' % (cols_size, rows_size))
    print()

    print((df.iloc[:, 1]))
    print('col values valid:', df.iloc[:, 1].notna().all())
    print()
    print((df.iloc[:, 5]))
    print('col values valid:', df.iloc[:, 5].notna().all())
    print()

    all_data = []
    for i in range(rows_size):
        row_list = []
        for j in range(cols_size):
            item = df.iloc[i, j]
            if pd.notna(item):
                row_list.append(item)

        if len(row_list) > 0:
            all_data.append(row_list)

    return all_data


def excel_demo02():
    data = read_all_data_excel()
    print('data:')
    for record in data:
        print(record)


if __name__ == '__main__':

    excel_demo02()
    print('excel read and post demo DONE.')
