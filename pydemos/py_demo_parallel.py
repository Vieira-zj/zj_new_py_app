# -*- coding: utf-8 -*-
'''
Created on 2019-03-14
@author: zhengjin

Python multiple process, threads and pool examples.
'''

import os
import sys
import time


# --------------------------------------------------------------
# Coroutine (协程)
# --------------------------------------------------------------
# example 01, generator
def py_parallel_demo01():
    import threading

    def generate_numbers(n):
        t_name = threading.current_thread().getName()
        print('[%s:%s] start to generate numbers' % (os.getpid(), t_name))
        for i in range(n):
            time.sleep(1)
            yield i

    numbers = generate_numbers(5)
    print('[%s:%s] main' % (os.getpid(), threading.current_thread().getName()))

    print('numbers:')
    print(next(numbers))
    print(next(numbers))
    for number in numbers:
        print(number)


# example 02, coroutine (协程), 生产消费模型
def py_parallel_demo02():
    import threading

    def consumer():
        tag = '[consumer-%s:%s]' % (os.getpid(), threading.currentThread().getName())
        print(tag + ' Start ...')
        yield 0

        while 1:
            ret_msg = '[%s] 200 OK' % time.strftime(r'%y-%m-%d:%H%M%S')
            item = yield ret_msg
            if not item:
                return
            print(tag + ' Consuming %s ...' % item)
            time.sleep(2)

    def producer(c):
        tag = '[producer-%s:%s]' % (os.getpid(), threading.currentThread().getName())
        if next(c) != 0:
            raise Exception('generator start failed!')

        for n in range(5):
            print(tag + ' Producing %s ...' % n)
            time.sleep(2)
            r = c.send(n)
            print(tag + ' Consumer return: %s' % r)

    # main
    c = consumer()
    try:
        producer(c)
    finally:
        if c:
            t_name = threading.currentThread().getName()
            print('[main-%s:%s] close generator' % (os.getpid(), t_name))
            c.close()


# --------------------------------------------------------------
# Threads (多线程)
# --------------------------------------------------------------
# example 03, 多线程 生产消费模型 condition (refer example_15)
def py_parallel_demo03():
    import threading

    class Producer(threading.Thread):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Producer (%s:%s)]' % (os.getpid(), self.name)

            while 1:
                if self.lock.acquire():
                    if self.products['value'] < 10:
                        try:
                            self.products['value'] += 1
                            print(tag, 'deliver one, now products: %d' % self.products['value'])
                            self.empty_cond.notify_all()  # 不释放锁
                            time.sleep(1)
                        finally:
                            if self.lock:
                                self.lock.release()
                    else:
                        print(tag, 'already 10, stop deliver, now products: %d' % self.products['value'])
                        self.full_cond.wait()  # 自动释放锁
                        print(tag, 'resume from wait')
                        # 这里没有调用release方法主动释放锁, 使用RLOCK, 可重新获得锁
                time.sleep(0.5)  # 让其他线程有机会获得锁
    # end class

    class Consumer(threading.Thread):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Consumer (%s-%s)]' % (os.getpid(), self.name)
            while 1:
                if self.lock.acquire():
                    if self.products['value'] > 1:
                        try:
                            self.products['value'] -= 1
                            print(tag, 'consume one, now products: %d' % self.products['value'])
                            self.full_cond.notify_all()
                            time.sleep(1)
                        finally:
                            if self.lock:
                                self.lock.release()
                    else:
                        print(tag, 'only 1, stop consume, products: %d' % self.products['value'])
                        self.empty_cond.wait()
                        print(tag, 'resume from wait')
                        # 这里没有调用release方法主动释放锁, 使用RLOCK, 可重新获得锁
                time.sleep(0.5)
    # end class

    # main
    products = {'value': 5}
    lock = threading.RLock()
    full_cond = threading.Condition(lock)
    empty_cond = threading.Condition(lock)

    for _ in range(1):
        p = Producer(products, lock, full_cond, empty_cond)
        p.start()
    for _ in range(3):
        c = Consumer(products, lock, full_cond, empty_cond)
        c.start()


# example 04, 多线程 线程间同步 condition
alist = None

def py_parallel_demo04():
    import threading

    def doSet(lock, condition):
        tag = 'Set [%s:%s]' % (os.getpid(), threading.currentThread().getName())
        with lock:
            print(tag, 'get lock')
            while alist is None:
                print(tag, 'list is not init, and wait')
                condition.wait()
            print(tag, 'resume from wait')
            time.sleep(1)
            for i in range(len(alist))[::-1]:
                alist[i] = 1
            print(tag, 'list modified')
            condition.notify()

    def doPrint(lock, condition):
        tag = '[Print (%s:%s)]' % (os.getpid(), threading.currentThread().getName())
        with lock:
            print(tag, 'get lock')
            while alist is None or sum(alist) == 0:
                print(tag, 'list is not ready, and wait')
                condition.wait()
            print(tag, 'resume from wait')
            time.sleep(1)
            for i in alist:
                print(tag, i)

    def doCreate(lock, condition):
        tag = '[Create (%s:%s)]' % (os.getpid(), threading.currentThread().getName())
        global alist
        with lock:
            print(tag, 'get lock')
            if alist is None:
                alist = [0 for _ in range(5)]
                time.sleep(1)
                print(tag, 'list init')
                condition.notifyAll()

    # main
    lock = threading.Lock()
    cond = threading.Condition(lock)

    threads = []
    threads.append(threading.Thread(target=doPrint, args=(lock, cond), name='t_print'))
    threads.append(threading.Thread(target=doSet, args=(lock, cond), name='t_set'))
    threads.append(threading.Thread(target=doCreate, args=(lock, cond), name='t_create'))
    # run workflow => doCreate, doSet, doPrint
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print('[%s:%s] main' % (os.getpid(), threading.currentThread().getName()))


# example 05, 多线程 生产消费模型 同步阻塞队列
def py_parallel_demo05():
    import random
    import threading
    from queue import Queue

    class Producer(threading.Thread):
        def __init__(self, q):
            self.queue = q
            super().__init__()

        def run(self):
            tag = 'Producer [%s:%s]' % (os.getpid(), threading.current_thread().getName())
            while 1:
                print(tag, 'is running ...')
                input_int = random.randint(0, 10)
                self.queue.put(input_int, block=True, timeout=10)
                print(tag, 'enqueue a number: %d, queue size: %d' % (input_int, self.queue.qsize()))
                time.sleep(2)

    class Consumer(threading.Thread):
        def __init__(self, q):
            self.queue = q
            super().__init__()

        def run(self):
            tag = 'Consumer [%s:%s]' % (os.getpid(), threading.current_thread().getName())
            while 1:
                print(tag, 'is running ...')
                output_init = self.queue.get(block=True, timeout=10)
                print(tag, 'dequeue a number: %d, queue size: %d' % (output_init, self.queue.qsize()))
                time.sleep(1)

    # main
    q = Queue(maxsize=10)
    for i in range(5):
        q.put(i)
    print('queue init size: %d' % q.qsize())

    for _ in range(1):
        Producer(q).start()
    for _ in range(2):
        Consumer(q).start()


# --------------------------------------------------------------
# Process (多进程)
# --------------------------------------------------------------
# example 11, 进程间共享数据 multiprocessing
def py_parallel_demo11():
    import multiprocessing

    def my_update(num, arr):
        print('[%s] my_update is running ...' % os.getpid())
        num.value = 14.1
        for i in range(len(arr)):
            arr[i] = -arr[i]
        time.sleep(1)

    num = multiprocessing.Value('d', 1.0)  # decimal
    arr = multiprocessing.Array('i', range(10))  # int
    p = multiprocessing.Process(target=my_update, args=(num, arr,))
    p.start()
    p.join()

    print('[%s] main is running ...' % os.getpid())
    print('number:', num.value)
    print('array:', arr[:])


# example 12, 进程间共享数据 multiprocessing.manager
def py_parallel_demo12():
    from multiprocessing import Process, Manager

    def my_update(lock, shareValue, shareList, shareDict):
        with lock:
            print('[%s] my_update is running ...' % os.getpid())
            shareValue.value += 1
            for i in range(len(shareList)):
                shareList[i] += 1
            shareDict['key1'] += 1
            shareDict['key2'] += 2
            time.sleep(1)

    manager = Manager()
    shareValue = manager.Value('i', 1)
    shareList = manager.list(range(5))
    shareDict = manager.dict({'key1': 1, 'key2': 2})

    lock = manager.Lock()
    procs = [Process(target=my_update, args=(lock, shareValue, shareList, shareDict)) for _ in range(10)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print('[%s] main is running ...' % os.getpid())
    print('share value:', shareValue.value)
    print('share list:', shareList)
    print('share dict:', shareDict)


# example 13, 进程间共享数据 multiprocessing.manager
def py_parallel_demo13():
    from multiprocessing import Process, Manager

    class MyProcess(Process):
        def __init__(self, lock, shareValue, shareList, shareDict):
            self.lock = lock
            self.shareValue = shareValue
            self.shareList = shareList
            self.shareDict = shareDict
            super().__init__()

        def run(self):
            with self.lock:
                print('[%s] MyProcess is running ...' % self.pid)
                self.shareValue.value += 1
                for i in range(len(self.shareList)):
                    self.shareList[i] += 1
                self.shareDict['key1'] += 1
                self.shareDict['key2'] += 2
                time.sleep(1)
    # end class

    # main
    manager = Manager()
    shareValue = manager.Value('i', 1)
    shareList = manager.list([1, 2, 3, 4, 5])
    shareDict = manager.dict({'key1': 1, 'key2': 2})
    lock = manager.Lock()

    procs = [MyProcess(lock, shareValue, shareList, shareDict) for _ in range(5)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print('[%s] main is running ...' % os.getpid())
    print('share value:', shareValue.value)
    print('share list:', shareList)
    print('share dict:', shareDict)


# example 14, 进程间共享数据 multiprocessing.manager
def py_parallel_demo14():
    from multiprocessing import Process, Value, Lock
    from multiprocessing.managers import BaseManager

    class Employee(object):
        def __init__(self, name, salary):
            self.name = name
            self.salary = Value('i', salary)

        def increase(self):
            self.salary.value += 100
            time.sleep(1)

        def getPay(self):
            return '%s,%d' % (self.name, self.salary.value)

    class MyManager(BaseManager):
        pass

    def incrSalary(lock, employee):
        with lock:
            print('[%s] incrSalary is running ...' % os.getpid())
            employee.increase()

    # main
    MyManager.register('Employee', Employee)
    manager = MyManager()
    manager.start()
    em = manager.Employee('Henry', 1000)

    lock = Lock()
    procs = [Process(target=incrSalary, args=(lock, em)) for _ in range(5)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print('[%s] main, Employee pay (%s)' % (os.getpid(), em.getPay()))


# example 15, 多进程 生产消费模型
def py_parallel_demo15():
    from multiprocessing import Process, Lock, Condition, Value

    class Producer(Process):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Producer (%s:%s)]' % (self.pid, self.name)
            while 1:
                with self.lock:
                    if self.products.value < 10:
                        self.products.value += 1
                        print(tag, 'deliver one, now products: %d' % self.products.value)
                        self.empty_cond.notify_all()  # 不释放锁定
                        time.sleep(1)
                    else:
                        print(tag, 'already 10, stop deliver, now products: %d' % self.products.value)
                        self.full_cond.wait()  # 自动释放锁定
                        print(tag, 'resume from wait')
                time.sleep(0.5)
    # end class

    class Consumer(Process):
        def __init__(self, products, lock, full_cond, empty_cond):
            self.products = products
            self.lock = lock
            self.full_cond = full_cond
            self.empty_cond = empty_cond
            super().__init__()

        def run(self):
            tag = '[Consumer (%s:%s)]' % (self.pid, self.name)
            while 1:
                with self.lock:
                    if self.products.value > 1:
                        self.products.value -= 1
                        print(tag, 'consume one, now products: %d' % self.products.value)
                        self.full_cond.notify_all()
                        time.sleep(1)
                    else:
                        print(tag, 'only 1, stop consume, products: %d' % self.products.value)
                        self.empty_cond.wait()
                        print(tag, 'resume from wait')
                time.sleep(0.5)
    # end class

    # main
    products = Value('i', 5)
    lock = Lock()
    full_cond = Condition(lock)
    empty_cond = Condition(lock)

    for _ in range(3):
        p = Producer(products, lock, full_cond, empty_cond)
        p.start()
    for _ in range(1):
        c = Consumer(products, lock, full_cond, empty_cond)
        c.start()


# example 16, 多进程 生产消费模型 同步阻塞队列
def py_parallel_demo16():
    import random
    from multiprocessing import Process, Queue

    class Producer(Process):
        def __init__(self, queue):
            self.queue = queue
            super().__init__()

        def run(self):
            tag = '[Producer (%s:%s)]' % (self.pid, self.name)
            while 1:
                print(tag, 'is running ...')
                input_num = random.randint(0, 10)
                self.queue.put(input_num, block=True, timeout=10)
                print(tag, 'enqueue a number into queue:', input_num)
                time.sleep(1)

    class Consumer(Process):
        def __init__(self, queue):
            self.queue = queue
            super().__init__()

        def run(self):
            tag = '[Consumer (%s:%s)]' % (self.pid, self.name)
            while 1:
                print(tag, 'is running ...')
                output_num = self.queue.get(block=True, timeout=10)
                print(tag, 'deque a number from queue:', output_num)
                time.sleep(2)

    # main
    queue = Queue(maxsize=11)
    for i in range(5):
        queue.put(i)

    for _ in range(3):
        Producer(queue).start()
    for _ in range(1):
        Consumer(queue).start()


# example 17, 多进程池 multiprocessing pool
def Foo_17(i):
    print('[%s] Foo is running ...' % os.getpid())
    time.sleep(1)
    return i + 100

def py_parallel_demo17():
    from multiprocessing import Process, Pool

    def Bar_17(arg):
        print('[%s] Bar is callback ...' % os.getpid())
        return arg

    # main
    res_list = []
    pool = Pool(3)
    try:
        # ballback exec in main process
        res_list = [pool.apply_async(func=Foo_17, args=(i,), callback=Bar_17) for i in range(10)]
    finally:
        if pool:
            pool.close()
            pool.join()
    print('[%s] main, results:' % os.getpid())
    print(','.join([str(res.get()) for res in res_list]))


# example 18, 多线程/多进程池 multiprocessing pool map
def multiple(x):
    import threading
    res = x * 2
    time.sleep(1)
    t_name = threading.current_thread().getName()
    print('[%s:%s] %d * 2 = %d' % (os.getpid(), t_name, x, res))
    return res

def py_parallel_demo18(is_thread=False):
    import threading
    from multiprocessing import Pool as ProcessPool
    from multiprocessing.dummy import Pool as ThreadPool

    pool = ThreadPool(3) if is_thread else ProcessPool(3)
    try:
        res = pool.map(multiple, [num for num in range(11)])
    finally:
        if pool:
            pool.close()
            pool.join()
    print('[%s:%s] main results:' % (os.getpid(), threading.current_thread().getName()))
    print(','.join([str(num) for num in res]))


# --------------------------------------------------------------
# Pool Executor (多线程/多进程池)
# --------------------------------------------------------------
# example 21, 多线程/多进程池 concurrent.futures
def load_url(url):
    import threading
    import urllib.request as request

    print('[%s:%s] running ...' % (os.getpid(), threading.current_thread().getName()))
    with request.urlopen(url, timeout=5) as conn:
        return '%r page is %d bytes' % (url, len(conn.read()))

def py_parallel_demo21(is_thread=False):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import ProcessPoolExecutor
    from concurrent.futures import wait

    workers_num = 3
    executor = ThreadPoolExecutor(max_workers=workers_num) \
        if is_thread else ProcessPoolExecutor(max_workers=workers_num)
    urls = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
    f_list = [executor.submit(load_url, url) for url in urls]
    res = wait(f_list, return_when='ALL_COMPLETED')
    assert(len(res.not_done) == 0)

    print('[%s:%s] main, results:' % (os.getpid(), threading.current_thread().getName()))
    for f in res.done:
        print(f.result())


# example 22, 多线程/多进程池 concurrent.futures map
def py_parallel_demo22(is_thread=False):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import ProcessPoolExecutor
    from concurrent.futures import wait

    urls = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
    executor = ThreadPoolExecutor() if is_thread else ProcessPoolExecutor(max_workers=3)
    results = executor.map(load_url, urls)
    for res in results:
        print(res)
    print('[%s:%s] main' % (os.getpid(), threading.current_thread().getName()))


# example 23, 多进程池 concurrent.futures callback
def get_page(url):
    import requests
    import threading

    t_name = threading.current_thread().getName()
    print('[%s:%s] get page <%s>' % (os.getpid(), t_name, url))
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError('error get %s, and return code %d' %(url, response.status_code))
    return {'url': url, 'text': response.text}

def py_parallel_demo23(is_thread=False):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import ProcessPoolExecutor

    def parse_page(res):
        res = res.result()
        t_name = threading.current_thread().getName()
        print('[%s:%s] parse page <%s>' % (os.getpid(), t_name, res['url']))
        parse_line = 'url %r, size: %s' % (res['url'], len(res['text']))
        print(parse_line)

        with open(os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/test.out'), 'a') as f:
            f.write(parse_line + '\n')

    # main
    executor = ThreadPoolExecutor() if is_thread else ProcessPoolExecutor(max_workers=3)
    urls = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
    for url in urls:
        # for process, func "get_page()" must be defined global
        executor.submit(get_page, url).add_done_callback(parse_page)
    executor.shutdown()
    print('[%s:%s] main' % (os.getpid(), threading.current_thread().getName()))


# example 22, 多线程/多进程池 异常处理
def checkfile_process(logger, file_path):
    import random
    import time

    logger.debug('[%d] is running ...' % os.getpid())
    time.sleep(random.randint(1, 4))
    if not os.path.exists(file_path):
        # NOTE: in sub process/thread, we can NOT see the raised Exception from console,
        # instead use Future.exception() to get error message,
        # or use Future.result() to directly raise Exception.
        raise FileNotFoundError('file not found: ' + file_path)
    logger.debug('file found:' + file_path)

def py_parallel_demo24(is_thread = False):
    import logging
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import ProcessPoolExecutor
    from concurrent.futures import wait

    sys.path.append(os.getenv('PYPATH'))
    from utils import Constants, LogManager

    LogManager.build_logger(Constants.LOG_FILE_PATH, stream_log_level=logging.DEBUG)
    logger = LogManager.get_logger()

    base_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')
    file_paths = [os.path.join(base_path, 'test_data.csv')]
    file_paths.append(os.path.join(base_path, 'test_log.txt'))
    file_paths.append(os.path.join(base_path, 'not_exist.txt'))

    workers_num = 3
    executor = ThreadPoolExecutor(max_workers=workers_num) \
        if is_thread else ProcessPoolExecutor(max_workers=workers_num)
    f_submit = [executor.submit(checkfile_process, logger, path)
                for path in file_paths]
    f_done = wait(f_submit, return_when='ALL_COMPLETED')

    for future in f_done.done:
        if future.exception() is None:
            if future.result() is not None:
                # if error, result() will directly raise Exception
                logger.debug('result: ' + future.result())
        else:
            logger.error('exception ===> ' + str(future.exception()))

    logger.debug('[%d] main process done.' % os.getpid())
    LogManager.clear_log_handles()


if __name__ == '__main__':

    py_parallel_demo24()
    print('python parallel demo DONE.')
