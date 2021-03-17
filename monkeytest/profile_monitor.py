# -*- coding: utf-8 -*-
'''
Created on 2018-11-19

@author: zhengjin
'''

import time
import os
import sys

sys.path.append(os.getenv('PYPATH'))
from utils import Constants, LogManager, AdbUtils, SysUtils


class ProfileMonitor(object):
    '''
    Android app profile monitor by iTest.
    Pre-conditions: APP under test is added into iTest, and set data collect interval configs (by manual), prefer 3s.
    '''

    __itest_pkg_name = 'iflytek.testTech.propertytool'
    __itest_boot_act = 'iflytek.testTech.propertytool.activity.BootActivity'
    __log_root_dir_path = '/sdcard/AndroidPropertyTool4'
    __hand_log_dir = 'handTest'
    __hand_log_dir_path = __log_root_dir_path + '/' + __hand_log_dir

    def __init__(self, itest_collect_interval):
        '''
        Constructor
        '''
        self.__is_stopped = True
        self.__logger = LogManager.get_logger()
        self.__sys_utils = SysUtils()
        self.__adb_utils = AdbUtils()
        # note: this value should be greater than interval config in iTest
        self.__wait_time_between_check = itest_collect_interval + 1

    # --------------------------------------------------------------
    # Start Monitor
    # --------------------------------------------------------------
    def start_monitor(self):
        self.__clear_itest_logs()
        self.__launch_itest()
        time.sleep(2)
        self.__click_itest_monitor_btn()
        time.sleep(1)
        if not self.__is_itest_logfile_created():
            raise Exception('start iTest monitor failed!')
        self.__is_stopped = False

    def __clear_itest_logs(self):
        cmd = 'adb shell "cd %s;rm -rf %s*"' \
            % (self.__log_root_dir_path, self.__hand_log_dir)
        if not self.__sys_utils.run_sys_cmd(cmd):
            raise Exception('clear iTest log files failed!')

    def __launch_itest(self):
        cmd = 'adb shell am start ' + self.__itest_pkg_name + '/' + self.__itest_boot_act
        self.__sys_utils.run_sys_cmd(cmd)

        for i in range(0, 3):
            if self.__adb_utils.is_package_on_top(self.__itest_pkg_name):
                return
            time.sleep(1)
        raise Exception('launch iTest app failed!')

    def __is_itest_logfile_created(self):
        cmd = 'adb shell "cd %s;ls|grep %s"' \
            % (self.__log_root_dir_path, self.__hand_log_dir)
        return len(self.__sys_utils.run_sys_cmd_and_ret_content(cmd)) != 0

    def __click_itest_monitor_btn(self):
        cmd = 'adb shell input tap 800 1880'
        return self.__sys_utils.run_sys_cmd(cmd)

    # --------------------------------------------------------------
    # Running Monitor
    # --------------------------------------------------------------
    def running_monitor(self, run_mins, is_end_with_stop=True, interval=15):
        run_secs = run_mins * 60
        start = time.perf_counter()
        while 1:
            time.sleep(interval)
            if not self.__is_itest_running():
                self.__logger.error('iTest process is NOT running!')
                return
            if time.perf_counter() - start >= run_secs and self.__is_itest_running():
                if is_end_with_stop:
                    self.stop_monitor()
                    self.__is_stopped = True
                return

    def __is_itest_process_running(self):
        cmd = 'adb shell "ps | grep %s"' % self.__itest_pkg_name
        if len(self.__sys_utils.run_sys_cmd_and_ret_content(cmd)) == 0:
            return False
        return True

    def __is_cpu_logfile_updated(self):
        before_record_time = self.__get_cpu_logfile_record_time()
        self.__logger.info('before time: ' + before_record_time)
        time.sleep(self.__wait_time_between_check)
        after_record_time = self.__get_cpu_logfile_record_time()
        self.__logger.info('after time: ' + after_record_time)
        return before_record_time != after_record_time

    def __get_cpu_logfile_record_time(self):
        file_name = 'cpuSystem.txt'
        cmd = 'adb shell "cd %s;tail -n 1 %s"' \
            % (self.__hand_log_dir_path, file_name)
        last_line = self.__sys_utils.run_sys_cmd_and_ret_content(cmd)
        return last_line.split()[0]  # record time

    def __is_itest_running(self):
        if self.__is_itest_process_running() and self.__is_cpu_logfile_updated():
            return True
        return False

    # --------------------------------------------------------------
    # Stop Monitor and pull logs
    # --------------------------------------------------------------
    def stop_monitor(self):
        if self.__is_stopped:
            return

        self.__launch_itest()
        time.sleep(2)  # wait to fix action failed
        self.__click_itest_monitor_btn()
        time.sleep(1)
        self.__force_stop_itest()
        self.__is_stopped = True

    def __force_stop_itest(self):
        cmd = 'adb shell am force-stop ' + self.__itest_pkg_name
        self.__sys_utils.run_sys_cmd(cmd)

    def __clear_local_itest_logs(self, dir_path):
        SysUtils.delete_files_in_dir(dir_path)

    def pull_itest_logfiles(self, local_save_path):
        if len(local_save_path) == 0:
            self.__logger.warn('skip dump iTest logs!')
            return

        self.__clear_local_itest_logs(os.path.join(local_save_path, self.__hand_log_dir))
        cmd = 'adb pull %s %s' % (self.__hand_log_dir_path, local_save_path)
        if not self.__sys_utils.run_sys_cmd(cmd):
            self.__logger.error('dump iTest logs failed!')


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)

    monitor = ProfileMonitor(3)
    monitor.start_monitor()
    monitor.running_monitor(0.5)  # minutes
    monitor.stop_monitor()
    time.sleep(1)
    monitor.pull_itest_logfiles(r'D:\JDTestLogs')

    LogManager.clear_log_handles()
    print('profile monitor test DONE.')
