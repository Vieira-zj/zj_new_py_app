# -*- coding: utf-8 -*-
'''
Created on 2020-05-28
@author: zhengjin
'''

# -----------------------------------
# LinkedList
# -----------------------------------


class LinkedListNode(object):

    def __init__(self):
        self._value = None
        self._next = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next_node):
        self._next = next_node


class LinkedList(object):

    def __init__(self):
        self._head = None
        self._last = None
        self._size = 0

    @property
    def head(self):
        return self._head

    def append(self, value):
        node = LinkedListNode()
        node.value = value
        if self._head is None:
            self._head = node
        else:
            self._last.next = node
        self._last = node

    def insert(self, value):
        """
        插入节点后保持有序（从小到大排序）。
        """
        cur = self._head
        node = LinkedListNode()
        node.value = value
        if cur is None:
            self._head = node
            self._last = node
            return

        # insert head
        if value < cur.value:
            node.next = self._head
            self._head = node
            return

        # base cur node, check next node
        while cur.next and (cur.next.value < value):
            cur = cur.next
        # insert tailer
        if not cur.next:
            cur.next = node
            self._last = node
        else:
            tmp = cur.next
            cur.next = node
            node.next = tmp

    def size(self):
        ret = 0
        cur = self._head
        # base cur node, check cur node
        while cur:
            ret += 1
            cur = cur.next
        return ret

    def __str__(self):
        ret_values = []
        cur = self._head
        while cur:
            ret_values.append(cur.value)
            cur = cur.next
        if len(ret_values) == 0:
            return 'null'
        return ','.join([str(val) for val in ret_values])


def test_linkedlist():
    l1 = LinkedList()
    for val in (4, 7, 10, 8, 3, 4, 1, 2, 20, 11):
        l1.append(val)
    print(l1)

    l2 = LinkedList()
    for val in (4, 7, 10, 8, 3, 4, 1, 2, 20, 4, 11, 39):
        l2.insert(val)
    print(l2)


def distinct_linkedlist(l: LinkedList):
    """
    从无序链表中移除重复项。
    """
    if not l.head:
        return l

    cur = l.head
    s = set()
    s.add(cur.value)
    # base cur node, check next node
    while cur.next:
        if cur.next.value in s:
            cur.next = cur.next.next
        else:
            s.add(cur.next.value)
            cur = cur.next


def test_distinct_linkedlist():
    case1 = (1, 2, 3, 4)
    case2 = (1, 2, 2, 3, 4, 4)
    case3 = (4, 4, 7, 7, 7, 10, 8, 3, 4, 8, 1, 2, 4, 20, 11, 7, 4, 20, 39, 39)
    for case in (case1, case2, case3):
        l = LinkedList()
        for val in case:
            l.append(val)
        distinct_linkedlist(l)
        print(l)
        assert l.size() == len(set(case))


# -----------------------------------
# Stack
# -----------------------------------


class Stack(object):

    def __init__(self):
        self.top = 0
        self.store_list = []

    def size(self):
        return len(self.store_list)

    def push(self, val):
        self.top += 1
        self.store_list.append(val)

    def pop(self):
        if self.top < 1:
            raise StackEmptyException()
        self.top -= 1
        return self.store_list.pop(self.size() - 1)

    def __repr__(self):
        if self.size() < 1:
            return '[]'
        return '[%s]' % (','.join(self.store_list))


class StackEmptyException(Exception):

    def __init__(self):
        self.value = 'stack is empty'

    def __str__(self):
        # return repr(self.value)
        return self.value


if __name__ == '__main__':

    # test_linkedlist()
    test_distinct_linkedlist()
    print('py struct base demo done.')
