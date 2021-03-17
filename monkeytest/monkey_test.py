# -*- coding: utf-8 -*-
'''
Created on 2018-10-29

@author: zhengjin
'''

import os
import subprocess
import time
import threading
import sys

sys.path.append(os.getenv('PYPATH'))
from utils import Constants, LogManager, AdbUtils, SysUtils
from monkeytest import MonkeyMonitor, ProfileMonitor, ChartParser, MonkeyReport


class MonkeyTest(object):
    '''
    Monkey test for APP, and collect APP and profile logs. 
    Pre-condition: login into APP before monkey test (by manual).
    '''

    # --------------------------------------------------------------
    # Init
    # --------------------------------------------------------------
    def __init__(self, test_pkg_name, run_mins):
        '''
        Constructor
        '''
        self.__test_pkg_name = test_pkg_name
        self.__run_mins = int(run_mins)

        cur_time = SysUtils.get_current_date_and_time()
        self.__log_root_path = os.path.join(os.getcwd(), 'monkeyreports')
        self.__log_dir_path_for_win = os.path.join(self.__log_root_path, cur_time)
        self.__log_dir_path_for_shell = '/data/local/tmp/monkey_test_logs'

        self.__exec_log_path = os.path.join(self.__log_dir_path_for_win, 'run_log.log')
        self.__device_props_file_path = os.path.join(self.__log_dir_path_for_win, 'device_props.log')
        self.__app_dump_file_path = os.path.join(self.__log_dir_path_for_win, 'app_info.log')
        self.__monkey_log_path_for_shell = '%s/%s' % (self.__log_dir_path_for_shell, 'monkey_log.log')
        self.__logcat_log_path_for_shell = '%s/%s' % (self.__log_dir_path_for_shell, 'logcat_full_log.log')

        self.__logcat_exception_file_name = 'logcat_exception.log'
        self.__logcat_exception_path_for_shell = '%s/%s' % (self.__log_dir_path_for_shell, self.__logcat_exception_file_name)
        self.__logcat_anr_file_name = 'logcat_anr.log'
        self.__logcat_anr_path_for_shell = '%s/%s' % (self.__log_dir_path_for_shell, self.__logcat_anr_file_name)
        
        SysUtils.create_dir(self.__log_dir_path_for_win)
        self.__logger = LogManager.build_logger(self.__exec_log_path)
        self.__sysutils = SysUtils()
        self.__adbutils = AdbUtils()
        self.__monitor = MonkeyMonitor()
        
        self.__profile_monitor = ProfileMonitor(Constants.ITEST_COLLECT_INTERVAL)
        self.__chart_parser = ChartParser(self.__log_dir_path_for_win)
        self.__report = MonkeyReport(self.__log_dir_path_for_win, self.__logcat_exception_file_name, self.__logcat_anr_file_name)

    # --------------------------------------------------------------
    # Monkey and logcat processes
    # --------------------------------------------------------------
    def __build_monkey_cmd(self):
        monkey_cmd = 'adb shell "monkey --throttle 500 -p %s' % self.__test_pkg_name

        monkey_launch_params = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c ' + \
            'android.intent.category.DEFAULT --monitor-native-crashes --kill-process-after-error'
        monkey_ignore = ''
        if Constants.IS_MONKEY_CRASH_IGNORE:
            monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes'
#         monkey_actions_pct = '--pct-touch 65 --pct-motion 20 --pct-trackball 5 --pct-nav 0 ' + \
#             '--pct-majornav 5 --pct-syskeys 5 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0'
        monkey_actions_pct = self.__build_monkey_action_cmd()
        monkey_format = '-v -v -v %s > %s"' % (Constants.MONKEY_TOTAL_RUN_TIMES, self.__monkey_log_path_for_shell)

        return ' '.join((monkey_cmd, monkey_launch_params, monkey_ignore, monkey_actions_pct, monkey_format))

    def __build_monkey_action_cmd(self):
        options = []
        options.append('--pct-touch ' + Constants.PCT_TOUCH)
        options.append('--pct-motion ' + Constants.PCT_MOTION)
        options.append('--pct-trackball ' + Constants.PCT_TRACKBALL)
        options.append('--pct-nav ' + Constants.PCT_NAV)
        options.append('--pct-majornav ' + Constants.PCT_MAJORNAV)
        options.append('--pct-syskeys ' + Constants.PCT_SYSKEYS)
        options.append('--pct-appswitch ' + Constants.PCT_APPSWITCH)
        options.append('--pct-anyevent ' + Constants.PCT_ANYEVENT)
        return ' '.join(options)

    def __run_monkey_subprocess(self):
        cmd = self.__build_monkey_cmd()
        self.__logger.info('Run monkey command: ' + cmd)
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def __run_logcat_subprocess(self):
        cmd = 'adb logcat -c && adb logcat -f %s -v threadtime *:%s' % (self.__logcat_log_path_for_shell, Constants.LOGCAT_LOG_LEVEL) 
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # --------------------------------------------------------------
    # Adb and Shell utils
    # --------------------------------------------------------------
    def __create_log_dir_for_shell(self, dir_path):
        self.__check_adb_action(self.__adbutils.create_dir_on_shell(dir_path))
        
    def __clear_log_dir_for_shell(self):
        self.__check_adb_action(self.__adbutils.remove_files_on_shell(self.__log_dir_path_for_shell))

    def __check_adb_action(self, lines):
        for line in lines:
            if 'busy' in line:
                self.__logger.error(line)
                raise Exception('Monkey test exit because of device busy!')
    
    def __filter_shell_logcat_exception(self):
        cmd = 'adb shell \"cat %s | grep \'at com.jd.b2b\' -C 20 > %s"' % (self.__logcat_log_path_for_shell, self.__logcat_exception_path_for_shell)
        if not self.__sysutils.run_sys_cmd(cmd):
            self.__logger.warning('Filter exception for logcat failed!')

    def __filter_shell_logcat_anr(self):
        cmd = 'adb shell \"cat %s | grep \'E ANRManager: ANR\' -C 20 > %s"' % (self.__logcat_log_path_for_shell, self.__logcat_anr_path_for_shell)
        if not self.__sysutils.run_sys_cmd(cmd):
            self.__logger.warning('Filter anr for logcat failed!')

    def __pull_all_testing_logs(self):
        shell_log_files = (self.__logcat_log_path_for_shell, self.__monkey_log_path_for_shell,
                           self.__logcat_exception_path_for_shell, self.__logcat_anr_path_for_shell)
        for shell_f in shell_log_files:
            cmd_pull_log_files = 'adb pull %s %s' % (shell_f, self.__log_dir_path_for_win)
            if not self.__sysutils.run_sys_cmd(cmd_pull_log_files):
                self.__logger.warning('Pull logcat file failed: ' + shell_f)

        if not self.__adbutils.dump_tombstone_files(self.__log_dir_path_for_win):
            self.__logger.warning('Pull tombstone file failed!')

        self.__pull_latest_anr_files()

    def __pull_latest_anr_files(self):
        '''
        Get anr files in 24 hours.
        '''
        cmd = 'adb shell "find /data/anr/ -name *.txt -mtime -1 2>/dev/null"'
        anr_files = self.__sysutils.run_sys_cmd_and_ret_lines(cmd)
        if len(anr_files) == 0:
            return
        
        save_path = os.path.join(self.__log_dir_path_for_win, 'anr')
        self.__sysutils.create_dir(save_path)
        for f in anr_files:
            f = f.strip('\r\n')
            if len(f) == 0:
                continue
            cmd = 'adb pull %s %s' % (f, save_path)
            if not self.__sysutils.run_sys_cmd(cmd):
                self.__logger.warning('Pull anr file failed: ' + f)
    
    # --------------------------------------------------------------
    # Create report and archive
    # --------------------------------------------------------------
    def __create_monkey_test_report(self):
        title_dict = {}
        title_dict['TEST PACKAGE'] = self.__test_pkg_name
        title_dict['RUN TIME (minutes)'] = str(self.__run_mins)
        self.__report.create_monkey_test_report(title_dict)
    
    def __create_archive_report_file(self):
        time.sleep(1)
        root_dir = r'D:\JDTestLogs'  # temp local save path
        target_file = os.path.join(root_dir, 'monkey_' + os.path.basename(self.__log_dir_path_for_win) + '.7z')
        cmd = r'"C:\Program Files\7-Zip\7z" a -t7z %s %s' % (target_file, self.__log_dir_path_for_win)

        self.__logger.debug('Create archive report file: ' + target_file)
        if not self.__sysutils.run_sys_cmd(cmd):
            self.__logger.warning('Create archive report file failed!')

    # --------------------------------------------------------------
    # Monkey Test Main
    # --------------------------------------------------------------
    def __is_profile_test_ok(self):
        return Constants.IS_PROFILE_TEST and int(self.__adbutils.get_android_version()[0]) < 7
    
    def __test_setup_main(self):
        if not self.__adbutils.is_devices_connected():
            raise Exception('No devices connected!')

        # shell env setup
        self.__adbutils.clear_anr_dir()
        self.__adbutils.clear_tombstone_dir()
        self.__clear_log_dir_for_shell()
        self.__create_log_dir_for_shell(self.__log_dir_path_for_shell)
    
        # win env setup
        self.__adbutils.dump_device_props(self.__device_props_file_path)
        self.__adbutils.dump_app_info(Constants.PKG_NAME_ZGB, self.__app_dump_file_path)
        
        if self.__is_profile_test_ok():
            self.__profile_monitor.start_monitor()

    def __test_main(self):
        self.__logger.info('Start logcat process.')
        logcat_p = self.__run_logcat_subprocess()
        self.__logger.info('Start monkey main process.')
        monkey_p = self.__run_monkey_subprocess()
    
        self.__logger.info('Start monkey monitor process.')
        monkey_monitor_t = threading.Thread(target=self.__monitor.process_monkey_monitor_main, args=(self.__run_mins,))
        threads = []
        threads.append(monkey_monitor_t)
        if self.__is_profile_test_ok():
            self.__logger.info('Start APP profile monitor process.')
            profile_monitor_t = threading.Thread(target=self.__profile_monitor.running_monitor, args=(self.__run_mins, False, Constants.WAIT_TIME_IN_LOOP))
            threads.append(profile_monitor_t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        monkey_p.kill()
        logcat_p.kill()

    def __test_clearup_main(self):
        # the adb connection maybe disconnect when running the monkey
        if self.__adbutils.is_devices_connected():
            self.__profile_monitor.stop_monitor()
            self.__adbutils.stop_app(self.__test_pkg_name)

            self.__filter_shell_logcat_exception()
            self.__filter_shell_logcat_anr()
            self.__pull_all_testing_logs()
            self.__create_monkey_test_report()

            if self.__is_profile_test_ok():
                time.sleep(1)
                self.__profile_monitor.pull_itest_logfiles(self.__log_dir_path_for_win)
                self.__chart_parser.build_all_profile_charts()
        else:
            self.__logger.error('Device disconnect!')
        LogManager.clear_log_handles()
    
        if Constants.IS_CREATE_ARCHIVE:
            self.__create_archive_report_file()
    
    def mokeytest_main(self):
        self.__test_setup_main()
        self.__test_main()
        self.__test_clearup_main()


if __name__ == '__main__':

    test = MonkeyTest(Constants.PKG_NAME_ZGB, Constants.RUN_MINS)
    test.mokeytest_main()
    print('Monkey test DONE.')
