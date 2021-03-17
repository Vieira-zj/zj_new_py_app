# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import os
import sys
import codecs
import time
import subprocess

sys.path.append(os.getenv('PYPATH'))
from utils import Constants
from utils import LogManager


class SysUtils(object):
    '''
    classdocs
    '''

    __sysutils = None

    @classmethod
    def get_instance(cls):
        if cls.__sysutils is None:
            cls.__sysutils = SysUtils()
        return cls.__sysutils

    def __init__(self):
        '''
        Constructor
        '''
        self.__logger = LogManager.get_logger()

    # --------------------------------------------------------------
    # Time functions
    # --------------------------------------------------------------
    @classmethod
    def get_current_date_and_time(cls):
        return time.strftime('%y-%m-%d_%H%M%S')

    @classmethod
    def get_current_date(cls):
        return time.strftime('%Y%m%d')

    @classmethod
    def get_current_date_with_sep(cls):
        return time.strftime('%Y-%m-%d')

    # --------------------------------------------------------------
    # Run system commands
    # --------------------------------------------------------------    
    def run_sys_cmd(self, cmd):
        self.__logger.debug('Exec command: ' + cmd)
        ret = os.system(cmd)
        if not ret == 0:
            self.__logger.warning('Failed, run command => %s, return code is %d' % (cmd, ret))
            return False
        return True
    
    def run_sys_cmd_and_ret_lines(self, cmd):
        self.__logger.debug('Exec command: ' + cmd)
        lines = os.popen(cmd).readlines()
        if len(lines) == 0:
            self.__logger.warning('The output is empty for command => ' + cmd)
        return lines

    def run_sys_cmd_and_ret_content(self, cmd):
        self.__logger.debug('Exec command: ' + cmd)
        content = os.popen(cmd).read()
        if content is None or content == '':
            self.__logger.warning('The output is empty for command => ' + cmd)
            content = ''
        return content.strip('\r\n')

    def run_sys_cmd_in_subprocess(self, cmd):
        self.__logger.debug('Exec command: ' + cmd)
    
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
    
        lines_error = p.stderr.readlines()
        lines_output = p.stdout.readlines()
        if len(lines_error) > 0:
            return lines_error
        if len(lines_output) > 0:
            return lines_output
        self.__logger.warning('The output is empty for command => ' + cmd)
        return ''

    # --------------------------------------------------------------
    # IO functions
    # --------------------------------------------------------------    
    @classmethod
    def create_dir(cls, path):
        if os.path.exists(path):
            return
        os.makedirs(path)

    @classmethod
    def delete_files_in_dir(cls, dir_path):
        if not os.path.exists(dir_path):
            return
        import shutil
        shutil.rmtree(dir_path)

    def read_lines_from_file(self, file_path):
        ret_lines = []
        if not os.path.exists(file_path):
            self.__logger.error('File is NOT exist: ' + file_path)
            return ret_lines
#             raise IOError('File not exist!')
        
        with codecs.open(file_path, 'r', 'utf-8') as f:
            ret_lines = f.readlines()
        return ret_lines

    def read_content_from_file(self, file_path):
        ret_content = ''
        if not os.path.exists(file_path):
            self.__logger.error('File is NOT exist: ' + file_path)
            return ret_content
#             raise IOError('File not exist!')
        
        with codecs.open(file_path, 'r', 'utf-8') as f:
            ret_content = f.read()
        return ret_content
    
    def write_lines_to_file(self, file_path, lines, is_override=True):
        if not self.__check_file_before_write(file_path, lines, is_override):
            return
    
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.writelines(lines)  # input lines should be unicode
            f.flush()
    
    def write_content_to_file(self, file_path, content, is_override=True):
        if not self.__check_file_before_write(file_path, content, is_override):
            return
            
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(content)
            f.flush()

    def __check_file_before_write(self, file_path, inputs, is_override):
        if len(inputs) == 0:
            self.__logger.error('The input is empty!')
            return False
        
        if os.path.exists(file_path): 
            if is_override:
                self.__logger.info('File (%s) is exist, and the inputs will be override!' % file_path)
            else:
                self.__logger.error('File (%s) is exist!' % file_path)
                return False
        return True


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)

#     SysUtils.delete_files_in_dir(r'D:\JDTestLogs\handTest')

    utils = SysUtils.get_instance()
    utils.run_sys_cmd('python --version')
    utils.write_content_to_file(Constants.TEST_FILE_PATH, 'test')

    LogManager.clear_log_handles()
    print('system utils test DONE.')
