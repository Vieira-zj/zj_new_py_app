# -*- coding: utf-8 -*-
'''
Created on 2019-01-08
@author: zhengjin

$ pip3 install kazoo

kazoo api reference:
https://kazoo.readthedocs.io/en/latest/api/client.html

watch可以通过两种方式设置: 
一种是在调用zk客户端方法的时候传递进去, 比如 zk.get_children("/node", watch=func), 
但是这种方法是一次性的, 也就是触发一次就没了, 如果你还想继续监听一个事件就需要再次注册.
另外一种方法是通过高级API实现, 监控数据或者节点变化, 它只需要我们注册一次, 在python里面就是kazoo. 
'''

import os
import sys
import time
import multiprocessing

from kazoo.client import KazooClient
from kazoo.client import ChildrenWatch
from kazoo.client import DataWatch


# --------------------------------------------------------------
# demo 01, zk watch api test
# --------------------------------------------------------------
def zk_test_01(url, test_node):
    # if run in multi process, should init a new zk client.
    zkc = KazooClient(hosts=url, timeout=3)
    zkc.start()

    print('\npid=%d, zookeeper version: %s' % (os.getpid(), zkc.server_version()))
    try:
        stat = zkc.set(test_node, b'zk_test_01_new_1')
        print('\nzk test node updated, and stat version:', stat.version)
        time.sleep(2)

        stat = zkc.set(test_node, b'zk_test_01_new_2')
        print('\nzk test node updated, and stat version:', stat.version)
        time.sleep(1)

        data, stat = zkc.get(test_node, watch=None)
        print('\nzk node stat:')
        print('\tnode data="%s", length=%d' % (data, stat.dataLength))
        print('\tnode stat version:', stat.version)
        print()
    finally:
        if zkc is not None:
            zkc.stop()


def zk_main_01():
    def _data_change(event):
        print('node data change [watch] =>')
        print('event type %s, path "%s"' % (event.type, event.path))

    url = '127.0.0.1:2181'
    test_node = '/zk_test_01'
    zkc = KazooClient(hosts=url, timeout=3)
    zkc.start()

    try:
        ret_path = zkc.create(path=test_node, value=b'zk_test_01_init')
        # watch func trigger only once
        if zkc.exists(ret_path, watch=_data_change):
            print('create zk node: ' + ret_path)
            time.sleep(1)

        p = multiprocessing.Process(target=zk_test_01, args=(url,test_node,))
        p.start()

        p.join(timeout=8)
        if p.is_alive():
            print('\npid=%d is pending, and kill!' % p.pid)
            p.kill()
    finally:
        if zkc.exists(test_node, watch=None):
            zkc.delete(test_node)
    zkc.stop()


# --------------------------------------------------------------
# zk demo 02, kazoo watch api test
# --------------------------------------------------------------
def zk_test_02(zkc, test_node):
    zkc.ensure_path(test_node)
    data, stat = zkc.get(test_node, watch=None)
    # data, stat = zkc.get(root_path, watch=_data_change)
    print('\nzk test node stat:')
    print('\tnode data:', data)
    print('\tnode stat version:', stat.version)
    print('\tnode stat number of children:', stat.numChildren)
    print()

    child_node_01 = test_node + '/test_child_01'
    ret_path = zkc.create(child_node_01, b'test_child_value_01')
    if ret_path is not None:
        print('\ncreate a child node:', ret_path)
        time.sleep(1)

    child_node_02 = test_node + '/test_child_02'
    ret_path = zkc.create(child_node_02, b'test_child_value_02', ephemeral=True)
    if ret_path is not None:
        print('\ncreate a ephemeral child node:', ret_path)
        # if no wait between changes, then it cannot trigger watch event
        time.sleep(1)

    stat = zkc.set(test_node, b'zk_test_02_new')
    print('\nzk test node updated, and stat version:', stat.version)
    time.sleep(1)

    if zkc.exists(child_node_01):
        if zkc.delete(child_node_01, recursive=False):
            print('\ndelete child node:', child_node_01)
    print('\nzk test node children:', zkc.get_children(test_node))


class zkWatcher(object):
    def __init__(self, url, test_node):
        self._url = url
        self._zk_node = test_node
        self._list_ori = []

    def exec(self):
        zkc = KazooClient(hosts=self._url, timeout=3)
        zkc.start()
        print('\npid=%d, zookeeper version: %s' % (os.getpid(), zkc.server_version()))

        try:
            self._list_ori = zkc.get_children(self._zk_node)

            print('\nattach data and child watch')
            # watch func trigger for each change
            DataWatch(client=zkc, path=self._zk_node, func=self._data_change)
            ChildrenWatch(client=zkc, path=self._zk_node, func=self._child_change)
            print('\nzk watch is running ...')
            time.sleep(6)
        finally:
            if zkc is not None:
                zkc.stop()

    def _data_change(self, data, stat):
        print('\nnode data change [watch] =>')
        print('\tnode data: %s, length: %d' % (data, stat.dataLength))
        print('\tstat version:', stat.version)
        print('\tnode number of children:', stat.numChildren)

    def _child_change(self, children):
        print('\nnode child change [watch] =>')
        if len(self._list_ori) > len(children):
            for child in self._list_ori:
                if child not in children:
                    print('\tdelete child node:', child)
                    break
        else:
            for child in children:
                if child not in self._list_ori:
                    print('\tadd child node:', child)
                    break
        self._list_ori = children
        print('zk test node cur children:', children)


def zk_main_02():
    url = '127.0.0.1:2181'
    zk_test_node = '/zk_test_02'
    zkc = KazooClient(hosts=url, timeout=3)
    zkc.start()
    print('\npid=%d, zookeeper version: %s' % (os.getpid(), zkc.server_version()))

    try:
        # ephemeral=False: cannot create child for ephemeral node
        ret_path = zkc.create(path=zk_test_node, value=b'zk_test_02_init', ephemeral=False)
        print('\ncreate a zk test node:', ret_path)
        time.sleep(1)

        zk_watcher = zkWatcher(url, zk_test_node)
        p = multiprocessing.Process(target=zk_watcher.exec)
        p.start()
        time.sleep(1)

        zk_test_02(zkc, zk_test_node)

        if p is not None:
            p.join(timeout=8)
            if p.is_alive():
                print('pid=%d is pending, and kill!' % p.pid)
                p.kill()
    finally:
        if zkc.exists(zk_test_node, watch=None):
            zkc.delete(zk_test_node, recursive=True)
        # close zk session, and all ephemeral nodes will be removed
        zkc.stop()


if __name__ == '__main__':

    # zk_main_01()
    zk_main_02()

    print('pid=%d, zookeeper test demo DONE.' % os.getpid())
