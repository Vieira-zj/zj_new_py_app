# -*- coding: utf-8 -*-
'''
Created on 2019-03-06
@author: zhengjin
'''

import os
import sys
import configparser

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.path.index(project_dir)
except ValueError:
    sys.path.append(project_dir)

from utils import Constants


def verify_configs(func):
    def _deco(*args, **kwargs):
        cls = args[0]
        if len(cls.configs) == 0:
            raise Exception('Pls load configs first!')
        return func(*args, **kwargs)
    return _deco

class LoadConfigs(object):

    SECTION_TEST_ENV = 'testenv'
    SECTION_MOCK = 'mockserver'
    SECTION_EMAIL = 'emails'

    configs = {}

    @classmethod
    def load_configs(cls, cfg_file_path):
        if len(cfg_file_path) == 0:
            raise ValueError('config file path is null!')
        if not os.path.exists(cfg_file_path):
            raise FileNotFoundError('configs file %s is not found!' % cfg_file_path)

        cfg_reader = configparser.ConfigParser()
        cfg_reader.read(cfg_file_path)

        for section in cfg_reader.sections():
            options = cfg_reader.options(section)
            tmp_dict = {}
            for option in options:
                tmp_dict[option] = cfg_reader.get(section, option)
            cls.configs[section] = tmp_dict

    @classmethod
    @verify_configs
    def get_testenv_configs(cls):
        return cls.configs.get(cls.SECTION_TEST_ENV)

    @classmethod
    @verify_configs
    def get_mock_configs(cls):
        return cls.configs.get(cls.SECTION_MOCK)

    @classmethod
    @verify_configs
    def get_email_configs(cls):
        return cls.configs.get(cls.SECTION_EMAIL)
# end class


if __name__ == '__main__':

    cfg_file_path = os.path.join(os.getenv('PYPATH'), 'apitest/configs.ini')
    LoadConfigs.load_configs(cfg_file_path)
    print('test http server url: %s:%s'
          % (LoadConfigs.get_mock_configs().get('ip'), LoadConfigs.get_mock_configs().get('port')))

    email_configs = LoadConfigs.get_email_configs()
    print('mail user pwd:', email_configs.get('mail_pwd'))
    print('mail content:', email_configs.get('content'))

    print('read ini configs DONE.')
