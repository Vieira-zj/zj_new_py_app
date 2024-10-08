# coding: utf-8

import random
from queue import Queue
from typing import List, Text

import gevent
from gevent.local import local
from gevent.pool import Group

group = Group()


def hello(n):
    gevent.sleep(3 - n)
    print('Size of group %s' % len(group))
    print('Hello %d from Greenlet %s' % (n, id(gevent.getcurrent())))
    return n


# ex1, Group().map()
def gevent_ex1():
    ''' greenlet 交替执行，但返回结果（list）与输入顺序一致 [0, 1, 2] '''
    res = group.map(hello, range(3))
    print(type(res), res)


# ex2, Group().imap()
def gevent_ex2():
    ''' 返回结果为IMap, 延迟执行 '''
    res = group.imap(hello, range(3))
    print(type(res), list(res))


# ex3, Group().imap_unordered()
def gevent_ex3():
    ''' greenlet 交替执行，先执行完成的先返回结果 [2, 1, 0] '''
    res = group.imap_unordered(hello, range(3))
    print(type(res), list(res))


# ex4, local var
class MyLocal(local):

    # 申明的属性将会穿透所有 greenlet 变成一个全局可读的属性（不再是 greenlet 本地的）
    __slots__ = ('number', 'x')
    initialized = False

    def __init__(self, **kw):
        if self.initialized:
            raise SystemError('__init__ called too many times')
        self.initialized = True
        self.__dict__.update(kw)

    def squared(self):
        return self.number ** 2


def gevent_ex4():
    stash = MyLocal()

    def func1():
        stash.x = 1
        stash.number = 3
        stash.z = 10
        print('z=%d' % stash.z)

        print('attributes:', [attr for attr in dir(
            stash) if not attr.startswith('__')])
        print('x=%d, number=%d' % (stash.x, stash.number))

    def func2():
        stash.y = 2
        print('y=%d' % stash.y)

        try:
            print('attributes:', [attr for attr in dir(
                stash) if not attr.startswith('__')])
            print('x=%d, number=%d' % (stash.x, stash.number))
        except AttributeError:
            print("x is not local to f2")

    g1 = gevent.spawn(func1)
    g2 = gevent.spawn(func2)
    gevent.joinall([g1, g2])


# ex5, get value from greenlet
def gevent_ex5():
    def ret_str(i: int):
        gevent.sleep(random.randint(0, 1))
        return str(i)

    # order
    g_list = []
    for i in range(1, 5):
        g = gevent.spawn(ret_str, i)
        group.add(g)
        g_list.append(g)

    if group.join():
        for g in g_list:
            print(g.value)

    # un order
    def ret_add(a, b):
        gevent.sleep(random.randint(0, 1))
        return a + b

    res = group.imap_unordered(ret_add, range(1, 5), range(1, 5))
    print(list(res))


# ex6, blocked queue
def gevent_ex6():
    def consume(q: Queue):
        while True:
            cmd = q.get()
            if cmd == 'stop':
                print('consume exit')
                return
            print(cmd)

    def product(q: Queue, values: List[Text]):
        for value in values:
            q.put(value)
            gevent.sleep(1)

    def test_with_threadpool():
        from concurrent.futures import ThreadPoolExecutor, wait

        q = Queue()
        values = 'this is a consume and product example, stop'.split(' ')

        executor = ThreadPoolExecutor()
        try:
            f1 = executor.submit(consume, q)
            f2 = executor.submit(product, q, values)
            done, not_done = wait((f1, f2), return_when='ALL_COMPLETED')
            print(f'done={len(done)}, not done={len(not_done)}')
        finally:
            if executor:
                executor.shutdown()

    def test_with_gevent():
        q = Queue()
        values = 'this is a consume and product example, stop'.split(' ')

        g1 = gevent.spawn(consume, q)
        g2 = gevent.spawn(product, q, values)
        gevent.joinall([g1, g2])

    is_threadpool = True
    if is_threadpool:
        test_with_threadpool()
    else:
        # notes: queue cannot be used with gevent
        test_with_gevent()


if __name__ == '__main__':

    gevent_ex6()
    print('gevent demo Done.')
