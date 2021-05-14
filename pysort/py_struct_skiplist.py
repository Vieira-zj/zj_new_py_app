# coding=utf-8

import math
import random


class Node(object):

    def __init__(self, key, value='', depth=1):
        self._key = key
        self._value = value
        self._depth = depth
        self._next = [None for _ in range(depth)]

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def depth(self):
        return self._depth

    def set_next_node(self, depth, node):
        if depth > (self._depth - 1):
            raise ValueError('available value: [0-%d]' % (self._depth - 1))
        self._next[depth] = node

    def get_next_node(self, depth):
        return None if depth > (self._depth - 1) else self._next[depth]

    def get_next_node_key(self, depth):
        return math.inf if depth > (self._depth - 1) or self._next[depth] is None else self._next[depth].key

    def __str__(self):
        return '%d:%s:%d' % (self.key, self.value, self.depth)


class SkipList(object):

    def __init__(self, max_depth, rate=0.5):
        self._rate = rate
        self._max_depth = max_depth
        self._root = Node(-math.inf, depth=max_depth)
        self._tail = Node(math.inf)
        self._depth = 1

        for i in range(self._max_depth):
            self._root.set_next_node(i, self._tail)

    def query(self, key) -> str:
        node = self._root
        for depth in range(self._depth - 1, -1, -1):
            while key > node.get_next_node_key(depth):
                node = node.get_next_node(depth)
            if key == node.get_next_node_key(depth):
                print('found at depth:', depth)
                return node.get_next_node(depth).value
        return ''

    def delete(self, key) -> bool:
        ret = False
        node = self._root
        for depth in range(self._depth - 1, -1, -1):
            while key > node.get_next_node_key(depth):
                node = node.get_next_node(depth)
            if key == node.get_next_node_key(depth):
                next_next_node = node.get_next_node(depth).get_next_node(depth)
                node.set_next_node(depth, next_next_node)
                if self._root.get_next_node_key(depth) == math.inf and self._depth > 1:
                    self._depth -= 1
                ret = True
        return ret

    def insert(self, key, value):
        node = self._root
        insert_nodes = []
        rand_depth = self._get_random_depth()
        for depth in range(rand_depth - 1, -1, -1):
            while key > node.get_next_node_key(depth):
                node = node.get_next_node(depth)
            if key == node.get_next_node_key(depth):
                print('update node: %d:%s:%d' % (key, value, depth))
                node.get_next_node(depth).value = value
                return
            insert_nodes.insert(0, node)

        new_node = Node(key, value, rand_depth)
        self._set_depth(rand_depth)
        print('insert new node:', str(new_node))
        for i in range(0, rand_depth):
            next_next_node = insert_nodes[i].get_next_node(i)
            insert_nodes[i].set_next_node(i, new_node)
            new_node.set_next_node(i, next_next_node)

    def print(self):
        for depth in range(self._depth - 1, -1, -1):
            values = []
            node = self._root
            while node.get_next_node_key(depth) != math.inf:
                node = node.get_next_node(depth)
                values.append(str(node))
            print('depth->%d: %s' % (depth, ','.join(values)))

    def _get_random_depth(self) -> int:
        depth = 1
        while True:
            r = random.random()
            if r < self._rate or depth == self._max_depth:
                return depth
            depth += 1

    def _set_depth(self, depth):
        if depth > self._depth:
            self._depth = depth


def skiplist_node_test():
    node1 = Node(1, "1", 2)
    node2 = Node(2, "2", 1)
    node1.set_next_node(3, node2)


def skiplist_test01():
    sl = SkipList(5)
    sl.insert(2, "2")
    sl.insert(1, "1")
    sl.insert(3, "3")
    print('\nupdate:')
    sl.insert(3, "3rd")
    sl.print()


def skiplist_test02():
    sl = SkipList(5)
    sl.insert(2, "2")
    sl.insert(1, "1")
    sl.insert(3, "3")
    sl.print()
    print('\ndelete:', sl.delete(2))
    sl.print()


def skiplist_test03():
    sl = SkipList(5)
    for value in (38, 55, 12, 31, 17, 50, 25, 44, 20, 39):
        sl.insert(value, str(value))
    sl.print()
    print(sl.query(39))


if __name__ == '__main__':

    # skiplist_node_test()
    # skiplist_test01()
    skiplist_test02()
    # skiplist_test03()
