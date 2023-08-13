# coding=utf-8

import inspect
from dataclasses import dataclass
from typing import Callable, Dict, List


def check():
    def _deco(fn):
        setattr(fn, 'is_target', True)
        return fn
    return _deco


@dataclass
class FnCallInfo:
    From: Callable
    To: Callable

    def __repr__(self) -> str:
        return f'FnCallsInfo(From={self.From.__name__}, To={self.To.__name__})'


def get_fn_calls_chain(fn: Callable) -> List[FnCallInfo]:
    vars_dict: Dict = inspect.getclosurevars(fn).globals
    fns: List[Callable] = [
        obj for obj in vars_dict.values() if isinstance(obj, Callable)]
    return [FnCallInfo(fn, sub_fn) for sub_fn in fns]


def build_fn_calls_chain():
    frame = inspect.currentframe()
    if frame is None:
        return

    print('cur frame:', frame)
    print('back frame:', frame.f_back)
    target_frame = frame.f_back or frame
    vars_dict = target_frame.f_globals
    result = []
    for obj in vars_dict.values():
        if isinstance(obj, Callable) and hasattr(obj, 'is_target'):
            result += get_fn_calls_chain(obj)
    return result

# test


def other_fn():
    print('other fn')


@check()
def a():
    pass


@check()
def c():
    pass


@check()
def b():
    print('b fn')
    a()
    c()


if __name__ == '__main__':

    print(get_fn_calls_chain(b))
    print()

    print(build_fn_calls_chain())
    print('done')
