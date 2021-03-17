# -*- coding: utf-8 -*-
'''
Created on 2018-10-26

@author: zhengjin
'''

import os
import sys
import logging

sys.path.append(os.getenv('PYPATH'))
from utils import Constants


class LogManager(object):
    '''
    classdocs
    '''

    __logger = None

    @classmethod
    def get_logger(cls):
        if cls.__logger is None:
            raise Exception('Pls init logger by build_logger() before use!')
        return cls.__logger

    @classmethod
    def build_logger(cls, log_path, stream_log_level=logging.INFO, file_log_level=logging.DEBUG):
        log_format_short = '%(asctime)s %(filename)s: [%(levelname)s] >>> %(message)s'
        log_format_long = '%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s]: %(message)s'
        date_format_short = '%d %b %H:%M:%S'
        date_format_long = '%a, %d %b %Y %H:%M:%S'

        # set stream handler
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(logging.Formatter(fmt=log_format_short, datefmt=date_format_short))
        sh.setLevel(stream_log_level)

        # set file handler
        fh = logging.FileHandler(filename=log_path, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter(fmt=log_format_long, datefmt=date_format_long))
        fh.setLevel(file_log_level)

        # logging.basicConfig(level=logging.NOTSET, format=log_format_short, datefmt=date_format_short)

        # init logger
        cls.__logger = logging.getLogger()
        # clear default log level WARN of basic configs
        # if not, it will override DEBUG and INFO level (WARN > INFO > DEBUG)
        cls.__logger.setLevel(logging.NOTSET)
        cls.__logger.addHandler(sh)
        cls.__logger.addHandler(fh)
        return cls.__logger

    @classmethod
    def clear_log_handles(cls):
        if cls.__logger is not None and cls.__logger.hasHandlers():
            for fh in cls.__logger.handlers:
                fh.close()
# end class


def sub_process(logger):
    import time
    time.sleep(1)
    print('in sub process')
    logger.info('info message test in sub process')


if __name__ == '__main__':

    import multiprocessing
    import threading

    logger = LogManager.build_logger(Constants.LOG_FILE_PATH)
    logger.debug('debug message test')
    logger.info('info message test')
    logger.warning('warning message test')

    # note: log from logging only print in thread but not process
    p1 = multiprocessing.Process(name='test_process', target=sub_process, args=(logger,))
    p1.start()
    p1.join()
    logger.info('process %s done' % p1.name)

    p2 = threading.Thread(name='test_thread', target=sub_process, args=(logger,))
    p2.start()
    p2.join()
    logger.info('process %s done' % p2.name)

    LogManager.get_logger().info('log utils test DONE.')
    LogManager.clear_log_handles()
