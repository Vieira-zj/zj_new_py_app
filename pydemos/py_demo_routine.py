# -*- coding: utf-8 -*-
'''
Created on 2019-03-31
@author: zhengjin
'''

import asyncio
import functools
import threading
import time


# demo01, start a routine
def py_routinue_demo01(loop):
    async def my_routinue():
        print('routinue is running ...')
        await asyncio.sleep(1)

    print('start a routinue')
    start = time.time()
    coro = my_routinue()
    print('run from event loop')
    loop.run_until_complete(coro)
    print('run time:', time.time() - start)


# demo02, return value from routine
def py_routinue_demo02(loop):
    async def my_routinue():
        print('routinue is running ...')
        await asyncio.sleep(1)
        return 'my_routinue_pass'

    result = loop.run_until_complete(my_routinue())
    print(f'get routinue result: {result}, default None')


# demo03, invoke 2 sub routines
def py_routinue_demo03(loop):
    async def routinue_main():
        print('this is main routine')
        print('wait for sub routine01 complete')
        ret1 = await routinue01()
        print('wait for sub routine02 complete')
        ret2 = await routinue02(ret1)
        return (ret1, ret2)

    async def routinue01():
        print('sub routine01 is running ...')
        await asyncio.sleep(0.5)
        return 'sub_routine01'

    async def routinue02(arg):
        print('sub routine02 is running ...')
        await asyncio.sleep(0.5)
        return f'sub_routine02 get argument: {arg}'

    print('start a routinue')
    coro = routinue_main()
    print('run in event loop')
    result = loop.run_until_complete(coro)
    print(f'get routinue result: {result}')


# demo04, invoke sync func by call_soon
def py_routinue_demo04(loop):
    def callback(args, *, kwargs='default'):
        print(f'sync callback, input args: {args}, {kwargs}')
        print('thread =>', threading.current_thread().getName())

    async def routine_main(loop):
        print('register callbacks')
        loop.call_soon(callback, 1)
        wrapped = functools.partial(callback, kwargs='not default')
        loop.call_soon(wrapped, 2)
        await asyncio.sleep(0.5)

    loop.run_until_complete(routine_main(loop))


# demo05, invoke sync func by call_later
def py_routinue_demo05(loop):
    def callback(n):
        print(f'sync callback {n} invoked')

    async def routine_main(loop):
        print('register callbacks')
        loop.call_later(0.3, callback, 3)
        loop.call_later(0.2, callback, 2)
        loop.call_soon(callback, 0)
        await asyncio.sleep(0.5)

    loop.run_until_complete(routine_main(loop))


# demo06, future
def py_routinue_demo06(loop):
    def foo(future, result):
        print('future status:', future)
        time.sleep(1)
        future.set_result(result)
        print('future status:', future)

    all_done = asyncio.Future()
    loop.call_soon(foo, all_done, 'future_test')
    print('loop is running:', loop.is_running())
    result = loop.run_until_complete(all_done)
    print('future returned result:', result)
    print('future.result:', all_done.result())


# demo07, await future
def py_routinue_demo07(loop):
    def foo(future, result):
        time.sleep(1)
        future.set_result(result)

    async def routine_main(loop):
        print('create future object')
        all_done = asyncio.Future()
        loop.call_soon(foo, all_done, 'future_await_test')
        print('loop is running:', loop.is_running())
        result = await all_done
        print('future returned result:', result)
        print('future.result:', all_done.result())

    loop.run_until_complete(routine_main(loop))


# demo08, future callback
def py_routinue_demo08(loop):
    def callback(future, n):
        print('[%s] future done: %s' % (n, future.result()))

    async def register_callbacks(all_done):
        print('register callback to future')
        all_done.add_done_callback(functools.partial(callback, n=1))
        all_done.add_done_callback(functools.partial(callback, n=2))

    async def routine_main(all_done):
        await register_callbacks(all_done)
        time.sleep(1)
        print('set result for future')
        all_done.set_result('future_callback_test')
        print('future status:', all_done)

    all_done = asyncio.Future()
    loop.run_until_complete(routine_main(all_done))
    print('future.result:', all_done.result())


# demo09, task
def py_routinue_demo09(loop):
    async def child():
        print('child routine is running ...')
        await asyncio.sleep(1)
        return 'child_pass'

    async def routine_main():
        print('wrapped routine to task')
        task = asyncio.create_task(child())
        # print('cancel task')
        # task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print('task cancel exception!')
        else:
            print('task done, and result:', task.result())

    loop.run_until_complete(routine_main())


# demo10, run multiple routines by wait
def py_routinue_demo10(loop):
    async def num(n):
        print(f'num {n} is running ...')
        try:
            await asyncio.sleep(n*0.1)
            return n
        except asyncio.CancelledError:
            print(f'num {n} is cancelled')
            raise

    async def routine_main():
        tasks = [num(i) for i in range(1, 11)]
        complete, pending = await asyncio.wait(tasks, timeout=0.5)
        for t in complete:  # asyncio.Task => t
            print('complete num:', t.result())
        if pending:
            print('cancel non complete task')
            for t in pending:
                t.cancel()

    loop.run_until_complete(routine_main())


# demo11, run multiple routines by gather
def py_routinue_demo11(loop):
    async def num(n):
        print(f'num {n} is running ...')
        try:
            await asyncio.sleep(n*0.1)
            return n
        except asyncio.CancelledError:
            print(f'num {n} is cancelled')
            raise

    async def routine_main():
        tasks = [num(i) for i in range(1, 11)]
        complete = await asyncio.gather(*tasks)
        for res in complete:
            print('complete num:', res)  # int => res

    start = time.time()
    loop.run_until_complete(routine_main())
    print('exec time:', time.time() - start)


# demo12, run multiple routines by as_completed
def py_routinue_demo12(loop):
    async def foo(n):
        print('wait:', n)
        await asyncio.sleep(n)
        return n

    async def routine_main():
        tasks = [asyncio.ensure_future(foo(i)) for i in range(1, 4)]
        for routine in asyncio.as_completed(tasks):
            result = await routine
            print('task result:', result)

    start = time.time()
    loop.run_until_complete(routine_main())
    print('exec time:', time.time() - start)


# demo13, routine in class
def py_routinue_demo13(loop):
    class MyClass(object):
        async def my_routine(self):
            print('my class-in routine is running ...')
            await asyncio.sleep(1)

    cls = MyClass()
    coro = cls.my_routine()
    loop.run_until_complete(coro)


# demo14, producer and consumer model
def py_routinue_demo14(loop):
    import asyncio

    class Producer(object):
        def __init__(self, goods):
            self.goods = goods

        async def goods_not_full(self):
            while self.goods['value'] >= 10:
                await asyncio.sleep(0.5)

        async def produce_good(self):
            tag = '[%s-Producer]' % threading.current_thread().getName()
            while 1:
                if self.goods['value'] < 10:
                    self.goods['value'] += 1
                    await asyncio.sleep(1)
                    print(tag, 'deliver one, now goods: %d' % self.goods['value'])
                else:
                    print(tag, 'already 10, stop deliver, now goods: %d' % self.goods['value'])
                    await self.produce_not_full()
                    print(tag, 'producer resume')
    # end class

    class Consumer(object):
        def __init__(self, goods):
            self.goods = goods

        async def goods_not_empty(self):
            while self.goods['value'] <= 1:
                await asyncio.sleep(0.5)

        async def consume_good(self):
            tag = '[%s-Consumer]' % threading.current_thread().getName()
            while 1:
                if self.goods['value'] > 1:
                    self.goods['value'] -= 1
                    await asyncio.sleep(0.5)
                    print(tag, 'consume one, now goods: %d' % self.goods['value'])
                else:
                    print(tag, 'only 1, stop consume, goods: %d' % self.goods['value'])
                    await self.goods_not_empty()
                    print(tag, 'consumer resume')
    # end class

    async def routine_main():
        goods = {'value': 5}
        tasks = []
        tasks.append(asyncio.create_task(Producer(goods).produce_good()))
        tasks.append(asyncio.create_task(Consumer(goods).consume_good()))

        _, pending = await asyncio.wait(tasks, timeout=15)
        if pending:
            print('cancel non complete task!')
            for t in pending:
                t.cancel()

    loop.run_until_complete(routine_main())


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        py_routinue_demo14(loop)
    finally:
        if loop:
            print('close event loop')
            loop.close()

    print('python coroutine demo DONE.')
