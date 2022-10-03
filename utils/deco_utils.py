# coding=utf-8

import time
import tracemalloc

from functools import wraps


def timer(fn):
    # 装饰器本身是用 @wraps(fn) 包裹的，这是为了确保传递包装函数。如果我们不这样做 wrapper.__name__ 只会打印 wrapper 而不是我们实际装饰的函数
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = fn(*args, **kwargs)
        duration = time.perf_counter() - start
        print('[%s] took %.2f ms' % (wrapper.__name__, duration * 1000))
        return res
    return wrapper


def perf_check(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        res = fn(*args, **kwargs)
        duration = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        lines = [f"{'-'*40}"]
        lines.append(f'Function:\t\t{fn.__name__} ({fn.__doc__})')
        lines.append(f'Memory usage:\t\t{current / 10**6:.6f} MB')
        lines.append(f'Peak memory usage:\t{peak / 10**6:.6f} MB')
        lines.append(f'Duration:\t\t{duration:.6f} sec')
        lines.append(f"{'-'*40}")
        print('\n'.join(lines))
        return res
    return wrapper


def repeater(iterations: int = 1):
    def outer_wrapper(fn):
        def wrapper(*args, **kwargs):
            res = None
            for _ in range(iterations):
                res = fn(*args, **kwargs)
            return res
        return wrapper
    return outer_wrapper


def prompt_sure(prompt_text: str):
    def outer_wrapper(fn):
        def wrapper(*args, **kwargs):
            if input(prompt_text).lower() != 'y':
                return
            return fn(*args, **kwargs)
        return wrapper
    return outer_wrapper


def try_catch(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f'Exception in [{fn.__name__}]: {e}')
    return wrapper

#
# Test
#


def test_timer():
    @timer
    def test_fn():
        time.sleep(2)
        print('test fn finish')

    test_fn()


def test_perf_check():
    @perf_check
    def is_prime(number: int) -> bool:
        isprime = False
        for i in range(2, number):
            if (number % i) == 0:
                isprime = True
                break
        return isprime

    print('is_prime(155153):', is_prime(155153))


def test_repeater():
    @repeater(iterations=2)
    def say_hello():
        print('hello')

    say_hello()


def test_prompt_sure():
    @prompt_sure('Sure? Press y to continue, press n to stop: ')
    def say_hi():
        print('hi')

    say_hi()


def test_try_catch():
    @try_catch
    def my_div(numa: int, numb: int):
        return numa / numb

    my_div(9, 3)
    my_div(9, 0)


if __name__ == '__main__':

    # test_timer()
    # test_perf_check()
    # test_repeater()
    # test_prompt_sure()
    test_try_catch()

    print('deco util done')
