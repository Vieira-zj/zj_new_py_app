# coding=utf-8

import sys
import os
sys.path.append(os.getenv('PYPROJECT'))

from pyapps.app_plugins_demo import main


@main.setup()
def log_params(context: dict):
    print('[info] func:', context['fn_name'])
    print('[info] input args:', context['args'])
    print('[info] input kwargs:', context['kwargs'])


@main.clearup()
def log_results(context: dict):
    print('[info] results:', context['results'])
