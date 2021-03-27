# -*- coding: utf-8 -*-
'''
Created on 2018-11-2
@author: zhengjin
'''

import signal
import threading

from monkeytest import MonkeyTest
from utils import Constants
from utils import AdbUtils
from utils import SysUtils


def test_mod_imports_01():
    '''
    define imports in monkeytest.__init__.py, and import py modules
    '''
    print('test file path:', Constants.TEST_FILE_PATH)
    print('\ncurrent date:', SysUtils.get_current_date())
    print('\nadb info:', AdbUtils.print_adb_info())


def test_mod_imports_02():
    from pydemos.imports import main
    main.run()


def test_mod_imports_03():
    from pydemos.py_demo_base import run_mod_imports
    run_mod_imports()


def run_monkey_test(args_kv):
    test = MonkeyTest(Constants.PKG_NAME_ZGB, args_kv.get(
        Constants.RUN_MINS_TEXT, Constants.RUN_MINS))
    test.mokeytest_main()


def cmd_args_parse():

    def __usage():
        lines = []
        lines.append('Usage:')
        lines.append('  $ python test_main.py -t 30')
        lines.append('Options:')
        lines.append(
            '  -t: time, monkey test run xx minutes. if not set, use RUN_MINS in constants.py as default.')
        lines.append('  -h: help')
        print('\n'.join(lines))

    import getopt
    import sys
    opts, _ = getopt.getopt(sys.argv[1:], 'ht:')

    ret_dict = {}
    if len(opts) == 0:
        # print usage and use default monkey test confs.
        __usage()
        return ret_dict

    for op, value in opts:
        if op == '-t':
            ret_dict.update({Constants.RUN_MINS_TEXT: value})
        elif op == '-h':
            __usage()
            exit(0)

    return ret_dict


def cmd_args_parse_v2():
    import argparse

    parser = argparse.ArgumentParser(prog='pydemo')

    parser.add_argument('-V', '--version', dest='version',
                        action='store_true', help='show version.')
    parser.add_argument('-v', dest='verbose', action='count',
                        default=0, help='show verbose log.')
    parser.add_argument('-c', '--config', dest='config',
                        help='config file path.')

    args = parser.parse_args()
    if hasattr(args, 'help'):
        parser.print_help()
        exit(1)

    return args


if __name__ == '__main__':

    # test_mod_imports_03()

    # args_dict = cmd_args_parse()
    # run_monkey_test(args_dict)

    args = cmd_args_parse_v2()

    if args.version:
        print('v1.0.0')
        exit(1)

    if args.verbose > 0:
        print('verbose level: %d' % args.verbose)

    if args.config and len(args.config):
        print('config file:', args.config)

    def signal_handler(signum, frame):
        threading.Event().set()
        print('ctrl-C pressed, and stop!')
        exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    print('wait for cancel...')
    threading.Event().wait()
