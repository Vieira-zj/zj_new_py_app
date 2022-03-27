# coding=utf-8

import functools
import importlib
import inspect
import time
import os

flag_is_setup = 'is_setup'
flag_is_clearup = 'is_clearup'

key_setup_funcs = 'setup_funcs'
key_clear_funcs = 'clear_funcs'

"""
NOTE:

setup, clearup 装饰器：
- 只包装了 func 函数，并没有执行（直接返回该函数）
- 被装饰的函数添加 @setup(), @clear() 注解
- 当 import 文件时，默认会执行（包装逻辑）

plugins 装饰器：
- 会执行 func 函数，并返回结果
- 使用 @plugins 注释
- 当文件 import 时，不会被执行。只有调用被装饰的 func 函数时，才会执行装饰器中的逻辑
"""


def setup():
    def _deco(fn):
        setattr(fn, flag_is_setup, True)
        return fn
    return _deco


def clearup():
    def _deco(fn):
        setattr(fn, flag_is_clearup, True)
        return fn
    return _deco


def plugins(fn):

    def _setup(context):
        if hasattr(fn, key_setup_funcs):
            setup_fns = getattr(fn, key_setup_funcs)
            for setup_fn in setup_fns:
                if inspect.isfunction(setup_fn):
                    setup_fn(context)

    def _clearup(context: str):
        if hasattr(fn, key_clear_funcs):
            clear_fns = getattr(fn, key_clear_funcs)
            for clear_fn in clear_fns:
                if inspect.isfunction(fn):
                    clear_fn(context)

    @functools.wraps(fn)  # fix issue fn name is changed to "_deco"
    def _deco(*args, **kwargs):
        import_plugins(fn)
        context = {'fn_name': fn.__name__, 'args': args, 'kwargs': kwargs}
        _setup(context)
        results = fn(*args, **kwargs)
        context = {'fn_name': fn.__name__, 'results': results}
        _clearup(context)
        return results

    return _deco


def import_plugins(main_fn):
    plugins_dir = 'pyapps/app_plugins_demo/plugins'
    dst_dir = os.path.join(os.getenv('PYPROJECT'), plugins_dir)
    py_files = []
    for f in os.listdir(dst_dir):
        if f.endswith('.py'):
            py_files.append({
                'name': os.path.splitext(f)[0],
                'path': os.path.join(dst_dir, f),
            })

    for item in py_files:
        name = item['name']
        path = item['path']
        source = importlib.machinery.SourceFileLoader(name, path)
        imported = source.load_module(name)

        for _, value in vars(imported).items():
            if inspect.isfunction(value):
                if hasattr(value, flag_is_setup):
                    append_plugins_funcs(main_fn, key_setup_funcs, value)
                elif hasattr(value, flag_is_clearup):
                    append_plugins_funcs(main_fn, key_clear_funcs, value)


def append_plugins_funcs(obj, key: str, fn):
    if not hasattr(obj, key):
        setattr(obj, key, [])
    fns = getattr(obj, key)
    fns.append(fn)

#
# main
#


@plugins
def my_process(text):
    import random
    time.sleep(random.randint(1, 5))
    return f'process pass: {text}'


def main():
    print('run:', my_process.__name__)
    res = my_process('mock')
    print('main:', res)


if __name__ == '__main__':

    main()
    pass
