# -*- coding: utf-8 -*-
'''
Created on 2018-10-30

@author: zhengjin
'''

import time
import os
import sys

sys.path.append(os.getenv('PYPATH'))
from utils import Constants, LogManager, AdbUtils


class MonkeyMonitor(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__logger = LogManager.get_logger()
        self.__adbutils = AdbUtils()

    def __get_monkey_process_id(self):
        return self.__adbutils.get_process_id_by_name('monkey')

    def __get_logcat_process_id(self):
        return self.__adbutils.get_process_id_by_name('logcat')

    def __wait_for_monkey_process_started(self):
        monkey_process_id = ''
        try_times = 3

        for i in range(0, try_times):
            time.sleep(3)
            monkey_process_id = self.__get_monkey_process_id()
            if len(monkey_process_id) > 0:
                break
        return monkey_process_id

    def process_monkey_monitor_main(self, run_mins, interval=Constants.WAIT_TIME_IN_LOOP):

        def _is_monkey_process_killed():
            return self.__get_monkey_process_id() == ''

        spec_run_time = int(run_mins) * 60
        interval = int(interval)

        if spec_run_time >= Constants.MAX_RUN_TIME:
            self.__logger.error(
                'Error, spec_time must be less than max_time (12 hours)!')
            exit(1)

        monkey_p_id = self.__wait_for_monkey_process_started()
        if monkey_p_id == '':
            self.__logger.error('Error, the monkey process is NOT started!')
            exit(1)

        # LOOP
        start = time.perf_counter()
        while 1:
            if _is_monkey_process_killed():
                self.__logger.error('Error, the monkey process is NOT running!')
                return

            current_time = time.perf_counter() - start
            self.__logger.info('Monkey is running... %d minutes and %d seconds' \
                % ((current_time / 60), (current_time % 60)))
            if (current_time >= spec_run_time) or (current_time >= Constants.MAX_RUN_TIME):
                self.__adbutils.kill_process_by_pid(monkey_p_id)
                self.__adbutils.kill_process_by_pid(self.__get_logcat_process_id())
                break
            time.sleep(interval)


if __name__ == '__main__':

    print('monkey monitor test DONE.')
