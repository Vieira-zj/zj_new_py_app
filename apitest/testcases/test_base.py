# -*- coding: utf-8 -*-
'''
Created on 2019-03-10
@author: zhengjin
'''

import pytest


class TestBase(object):

    CASE_SCHEMA_METHOD = 'Method'
    CASE_SCHEMA_HEADER = 'Headers'
    CASE_SCHEMA_URL = 'Url'
    CASE_SCHEMA_QUERY = 'Query'
    CASE_SCHEMA_BODY = 'Body'
    CASE_SCHEMA_RET_CODE = 'RetCode'
    CASE_SCHEMA_EXP_MSG = 'RetMsg'

    def base_http_assert(self, resp, retCode=200):
        assert(resp is not None and resp.status_code == retCode)
# TestBase end


@pytest.mark.usefixtures('setup_test_session')
class TestFixturesInit(object):

    def test_fixtures_init(self):
        pass
# TestFixturesInit end
