# coding=utf-8

import contextlib
import random
import time
from collections.abc import Iterator
from typing import Generator


class Dispatch(Iterator):
    """
    Get target_count of numbers at specified numbers_per_iter.
    """

    def __init__(self, target_count: int, numbers_per_iter: int):
        self._numbers_per_iter = numbers_per_iter
        self._iter_num = int(target_count / numbers_per_iter)
        self._instance: Generator[int, None, None] = self._new_dispatch()

    def _new_dispatch(self) -> Generator[int, None, None]:
        for _ in range(self._iter_num):
            with self._wait_between_dispatch_iteration_context():
                tmp = random.randint(1, 100)
                for j in range(self._numbers_per_iter):
                    yield tmp + j

    @contextlib.contextmanager
    def _wait_between_dispatch_iteration_context(self):
        # before enter
        yield
        # after exit
        print('wait...')
        time.sleep(1)  # default 1 sec

    def __next__(self) -> int:
        return next(self._instance)


if __name__ == '__main__':

    # get 15 numbers at rate 3/s
    dispatch = Dispatch(15, 3)
    for i in dispatch:
        print(i)

    print('dispatch done')
