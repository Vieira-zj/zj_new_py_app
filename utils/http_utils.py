# -*- coding: utf-8 -*-
'''
Created on 2019-03-06

@author: zhengjin
'''

import base64
import os
import sys
import json
import requests

sys.path.append(os.getenv('PYPATH'))
from utils import LogManager
from utils import Constants


class HttpUtils(object):

    HTTP_METHOD_GET = 'get'
    HTTP_METHOD_POST_DATA = 'post'
    HTTP_METHOD_POST_JSON = 'post_json'

    __http = None

    @classmethod
    def get_instance(cls):
        if cls.__http is None:
            cls.__http = HttpUtils()
        return cls.__http

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__headers = {}

    def set_default_headers(self, headers):
        self.__headers = headers
        return self

    def send_http_request(self, method, url, data, headers={}, timeout=1, is_log_body=True):
        if method == self.HTTP_METHOD_GET:
            return self.__send_get_request(url, data, headers, timeout, is_log_body)
        elif method == self.HTTP_METHOD_POST_DATA:
            return self.__send_post_request_data(url, data, headers, timeout, is_log_body)
        elif method == self.HTTP_METHOD_POST_JSON:
            return self.__send_post_request_json(url, data, headers, timeout, is_log_body)
        else:
            raise ValueError('invalid http request method!')

    # --------------------------------------------------------------
    # Http Get Request
    # --------------------------------------------------------------
    def __send_get_request(self, url, query, headers, timeout, is_log_body):
        self.__append_headers(headers)

        data_dict = {}
        if len(query) > 0:
            for entry in query.split('&'):
                k, v = entry.split('=')
                data_dict[k] = v

        resp = None
        try:
            self.__log_request_info(url, query, self.__headers)
            resp = requests.get(url, params=data_dict, headers=self.__headers, timeout=timeout)
            self.__log_response_info(resp, is_log_body)
        except TimeoutError:
            self.__logger.error('http get request time out(%ds)!' % timeout)

        return resp

    # --------------------------------------------------------------
    # Http Post Request
    # --------------------------------------------------------------
    def __send_post_request_data(self, url, data, headers, timeout, is_log_body):
        self.__append_headers(headers)

        resp = None
        try:
            self.__log_request_info(url, data, self.__headers)
            resp = requests.post(url, headers=self.__headers, data=data, timeout=timeout)
            self.__log_response_info(resp, is_log_body)
        except TimeoutError:
            self.__logger.error('http post request time out(%ds)!' % timeout)

        return resp

    def __send_post_request_json(self, url, json_object, headers, timeout, is_log_body):
        self.__append_headers(headers)

        resp = None
        try:
            self.__log_request_info(url, json.dumps(json_object), self.__headers)
            resp = requests.post(url, headers=self.__headers, json=json_object, timeout=timeout)
            self.__log_response_info(resp, is_log_body)
        except TimeoutError:
            self.__logger.error('http post request time out(%ds)!' % timeout)

        return resp

    def __append_headers(self, headers):
        for key in headers.keys():
            self.__headers[key] = headers[key]

    # --------------------------------------------------------------
    # Print Logs
    # --------------------------------------------------------------
    def __log_request_info(self, url, data, headers={}):
        self.__logger.debug('\n\n')
        self.__print_div_line()
        self.__print_with_prefix('Request: ' + url)

        self.__print_div_line()
        self.__print_with_prefix('Headers:')
        for item in ['%s: %s' % (k, v) for k, v in headers.items()]:
            self.__print_with_prefix(item)

        self.__print_div_line()
        if data.startswith('{'):
            self.__print_with_prefix('Body: \n' + data[:512])
        else:
            self.__print_with_prefix('Query: ' + data)

        self.__print_div_line()
        self.__print_with_prefix('END')

    def __log_response_info(self, resp, is_log_body=True):
        self.__print_div_line()
        self.__print_with_prefix('Url: ' + resp.url)
        self.__print_with_prefix('Status Code: %d' % resp.status_code)

        self.__print_div_line()
        self.__print_with_prefix('Headers:')
        for item in ['%s: %s' % (k, v) for k, v in resp.headers.items()]:
            self.__print_with_prefix(item)

        self.__print_div_line()
        content = 'null'
        if is_log_body:
            try:
                content = resp.content.decode(encoding='utf-8')
            except UnicodeDecodeError as _:
                try:
                    content = resp.content.decode(encoding='gbk')
                except UnicodeDecodeError as _:
                    content = str(base64.b64encode(resp.content))
        self.__print_with_prefix('Body: \n' + content[:1024])

        self.__print_div_line()
        self.__print_with_prefix('END')

    def __print_div_line(self):
        self.__print_with_prefix('-'*60)

    def __print_with_prefix(self, text):
        self.__logger.debug('* ' + text)


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)

    # get request
    headers = {'X-Test-Method': 'X-Test-Get'}
    http_utils = HttpUtils.get_instance().set_default_headers(headers)

    mock_url = 'http://127.0.0.1:17891/index'
    headers['Content-Type'] = 'text/plain; charset=utf-8'
    query = 'k1=v1&k2=v2'
    resp = http_utils.send_http_request(
        HttpUtils.HTTP_METHOD_GET, mock_url, query, headers=headers, timeout=0.5)
    assert(resp is not None and resp.status_code == 200)

    # post request
    headers = {'X-Test-Method': 'X-Test-Post'}
    http_utils.set_default_headers(headers)

    headers['Content-Type'] = 'text/json; charset=utf-8'
    data_dict = {'email': '123456@163.com', 'password': '123456'}
    # resp = http_utils.send_http_request(
    #     HttpUtils.HTTP_METHOD_POST_DATA, mock_url, json.dumps(data_dict), headers=headers)
    resp = http_utils.send_http_request(
        HttpUtils.HTTP_METHOD_POST_JSON, mock_url, data_dict, headers=headers)
    assert(resp is not None and resp.status_code == 200)

    LogManager.clear_log_handles()
    print('http utils test DONE.')
