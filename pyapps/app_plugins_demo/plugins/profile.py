# coding=utf-8

import sys
import os
sys.path.append(os.getenv('PYPROJECT'))

from datetime import datetime as dt
from pyapps.app_plugins_demo import main

start = None


@main.setup()
def profile_start(context: dict):
    global start
    start = dt.now()


@main.clearup()
def profile_end(context: dict):
    delta = dt.now() - start
    print(f'[{context["fn_name"]}] profile: {delta.seconds}')
