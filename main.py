# -*- coding: utf-8 -*-
'''
Created on 2018-11-2
@author: zhengjin
'''

import os
import sys
import signal
import subprocess
import threading
import traceback

from pathlib import Path
from monkeytest import MonkeyTest
from pyapps.app_cicd_tools import JenkinsTools, GitlabTool
from utils import Constants, AdbUtils, SysUtils

#
# py test
#


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


def run_py_demo():
    cur_dir = Path.resolve(Path(__file__)).parent
    py_file = Path.joinpath(cur_dir, 'pydemos', 'py_demo_base.py')
    cmd = ' '.join([sys.executable, str(py_file)])

    print('exec:', cmd)
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
    p.wait()

    output = p.stdout.read()
    print(output.decode(encoding='utf-8'))  # bytes to string

#
# py app test
#


def run_monkey_test(args_kv):
    test = MonkeyTest(Constants.PKG_NAME_ZGB, args_kv.get(
        Constants.RUN_MINS_TEXT, Constants.RUN_MINS))
    test.mokeytest_main()


def test_cicd():
    """
    1. 基于 jenkins job 的 git build data 获取 commit 信息
    2. 比较两个 job 的 commit 信息，获取 commit 提交历史
    """
    job = os.getenv('JENKINS_JOB')
    if not job:
        print('env var [JENKINS_JOB] is not set.')
        exit(99)

    # get commit/tag in job builds
    jenkins_tool = JenkinsTools()
    build_no = jenkins_tool.get_lastbuild_number(job)
    new_build_result = jenkins_tool.get_build_info(job, build_no)
    print('new build:\n', new_build_result)
    old_build_result = jenkins_tool.get_build_info(job, build_no - 7)
    print('old build:\n', old_build_result)

    # init gitlab tool
    gitlab_url = os.getenv('GITLAB_URL')
    private_token = os.getenv('GITLAB_PRIVATE_TOKEN')

    repo_url = new_build_result['git_build_data']['remote_url']
    prj_name = repo_url.split('/')[1][:-4]
    git_tool = GitlabTool(gitlab_url, private_token)
    git_tool.set_project(prj_name)
    print('\nproject:')
    git_tool.print_project_info()

    # diff commits between jobs, and get commits history
    new_commit_id = new_build_result['git_build_data']['commit_id'][:8]
    old_commit_id = old_build_result['git_build_data']['commit_id'][:8]
    print(f'\ncompare two commit: {old_commit_id} => {new_commit_id}')
    result = git_tool.compare_two_commits(old_commit_id, new_commit_id)

    diff_commits = result['commits']
    diffs = result['diffs']
    print('\ndiff commits count %d, diff files count %d' %
          (len(diff_commits), len(diffs)))

    # get diff commits for uat branch
    res_commits = git_tool.filter_commits_by_branch(diff_commits, 'uat')
    print('\ndiff commits for uat br count:', len(res_commits))
    print('commits:')
    for commit in res_commits:
        print(commit['short_id'], commit['title'])

#
# main
#


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
    parser.add_argument('-t', '--test', dest='test',
                        action='store_true', help='run test demo.')
    parser.add_argument('-s', '--signal', dest='isSignal',
                        action='store_true', help='run and wait for signal.')

    args = parser.parse_args()
    if hasattr(args, 'help'):
        parser.print_help()
        exit(1)
    return args


def main():
    # args_dict = cmd_args_parse()
    args = cmd_args_parse_v2()
    if args.version:
        print('v1.0.0')
        exit(1)

    if args.verbose > 0:
        print('verbose level: %d' % args.verbose)

    if args.config and len(args.config):
        print('config file:', args.config)

    if args.test:
        # test_mod_imports_03()
        # run_py_demo()

        # run_monkey_test(args_dict)
        test_cicd()

    if args.isSignal:
        def signal_handler(signum, frame):
            threading.Event().set()
            print('ctrl-C pressed, and stop.')
            exit(1)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        print('wait for cancel...')
        threading.Event().wait()

    print('main done')


if __name__ == '__main__':

    try:
        main()
    except:
        traceback.print_exc()
