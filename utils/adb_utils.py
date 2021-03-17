#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import sys
import os
import re

sys.path.append(os.getenv('PYPATH'))
from utils import Constants
from utils import LogManager
from utils import SysUtils


class AdbUtils(object):

    __adb = None

    @classmethod
    def get_instance(cls):
        if cls.__adb == None:
            cls.__adb = AdbUtils()
        return cls.__adb

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__sys_utils = SysUtils.get_instance()

    @classmethod
    def print_adb_info(cls):
        cmd = 'adb version'
        return os.popen(cmd).read()

    def start_app(self, app_launch_info):
        cmd = 'adb shell am start -S ' + app_launch_info
        return self.__sys_utils.run_sys_cmd(cmd)
    
    def stop_app(self, package_name):
        cmd = 'adb shell am force-stop ' + package_name
        return self.__sys_utils.run_sys_cmd(cmd)

    def clear_app_data(self, pkg_name):
        cmd = 'adb shell pm clear %s' % pkg_name
        return self.__sys_utils.run_sys_cmd(cmd)

    def is_devices_connected(self):
        # support one device
        self.__logger.debug('check adb devices connected.')
        
        cmd = 'adb devices -l'
#         cmd = 'adb get-serialno'
        ret_content = self.__sys_utils.run_sys_cmd_and_ret_content(cmd)
        if len(ret_content.strip()) == 0:
            return False
        if re.search('unknown|error|offline', ret_content):
            return False
        self.__logger.info('connected devices: \n%s', ret_content)
        return True

    def is_package_on_top(self, pkg_name):
        cmd = 'adb shell "dumpsys activity | grep mFocusedActivity | grep %s"' % pkg_name
        ret_content = self.__sys_utils.run_sys_cmd_and_ret_content(cmd)
        return len(ret_content) != 0

    def dump_app_info(self, app_name, file_path):
        if os.path.exists(file_path):
            self.__logger.warning('file %s is exist and will be override!' % file_path)
        cmd = 'adb shell dumpsys package %s > %s' % (app_name, file_path)
        return self.__sys_utils.run_sys_cmd(cmd)

    def get_android_version(self):
        cmd = 'adb shell "getprop | grep \'ro.build.version.release\' | cut -f 2 -d \' \'"'
        ret_content = self.__sys_utils.run_sys_cmd_and_ret_content(cmd)
        return ret_content.lstrip('[').rstrip(']')

    def dump_device_props(self, file_path):
        if os.path.exists(file_path):
            self.__logger.warning('file %s is exist and will be override!' % file_path)
        cmd = 'adb shell getprop > %s' % file_path
        return self.__sys_utils.run_sys_cmd(cmd)

    def dump_logcat_by_tag(self, tag, file_path):
        cmd = 'adb logcat -c && adb logcat -s %s -v time -d > %s' % (tag, file_path)
        return self.__sys_utils.run_sys_cmd(cmd)

    def dump_anr_files(self, save_path):
        cmd = 'adb pull /data/anr %s' % save_path
        return self.__sys_utils.run_sys_cmd(cmd)

    def clear_anr_dir(self):
        cmd = 'adb shell "rm -f /data/anr/* 2>/dev/null"'
        return self.__sys_utils.run_sys_cmd(cmd)

    def dump_tombstone_files(self, save_path):
        cmd = 'adb pull /data/tombstones %s' % save_path
        return self.__sys_utils.run_sys_cmd(cmd)

    def clear_tombstone_dir(self):
        cmd = 'adb shell "rm -f /data/tombstones/* 2>/dev/null"'
        return self.__sys_utils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # Process handle function
    # --------------------------------------------------------------
    def get_process_id_by_name(self, p_name):
        cmd = 'adb shell ps | findstr %s' % p_name
        for line in os.popen(cmd).readlines():
            if p_name in line:
                return line.split()[1]  # process id
        return ''

    def kill_process_by_pid(self, p_id):
        if p_id is None or len(p_id) == 0:
            return
        cmd = 'adb shell kill %s' % p_id
        return self.__sys_utils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # IO function
    # --------------------------------------------------------------
    def create_dir_on_shell(self, dir_path):
        cmd = 'adb shell "mkdir %s 2>/dev/null"' % dir_path
        return self.__sys_utils.run_sys_cmd_and_ret_lines(cmd)

    def remove_files_on_shell(self, file_path):
        cmd = 'adb shell "rm -rf %s 2>/dev/null"' % file_path
        return self.__sys_utils.run_sys_cmd_and_ret_lines(cmd)


if __name__ == '__main__':

    logger = LogManager.build_logger(Constants.LOG_FILE_PATH)

    utils = AdbUtils.get_instance()
    if utils.is_devices_connected():
        logger.info('Monkey pid:', utils.get_process_id_by_name('monkey'))
        logger.info('android version:', utils.get_android_version())
    else:
        logger.info('no adb device connect!')

    LogManager.clear_log_handles()
    print('adb manager test DONE.')
