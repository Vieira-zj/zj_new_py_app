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
        if not self._head:
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
        if not cur:
            self._head = node
            self._last = node
            return

        if value < cur.value:
            node.next = self._head
            self._head = node
            return

        while cur.next is not None and (cur.next.value < value):
            cur = cur.next
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
        while cur:
            cur = cur.next
            ret += 1
        return ret

    def __str__(self):
        cur = self._head
        if not cur:
            return 'null'

        ret_values = [cur.value]
        while cur.next:
            ret_values.append(cur.next.value)
            cur = cur.next
        return ','.join([str(val) for val in ret_values])


def linkedlist_test():
    l1 = LinkedList()
    for val in (4, 7, 10, 8, 3, 4, 1, 2, 20, 11):
        l1.append(val)
    print(l1)

    l2 = LinkedList()
    for val in (4, 7, 10, 8, 3, 4, 1, 2, 20, 11, 39):
        l2.insert(val)
    print(l2)


def distinct_linkedlist(l: LinkedList):
    """
    从无序链表中移除重复项。
    """
    if not l.head:
        return l

    cur = l.head
    d = {}
    d[cur.value] = 1
    while cur.next is not None:
        tmp = d.get(cur.next.value, 0)
        if tmp == 1:
            if not cur.next.next:
                cur.next = None
                return l
            else:
                cur.next = cur.next.next
        else:
            d[cur.next.value] = 1
            cur = cur.next


def distinct_linkedlist_test():
    cases = [(1, 2, 3, 4)]
    cases.append((1, 2, 2, 3, 4, 4))
    cases.append((4, 4, 7, 7, 7, 10, 8, 3, 4, 8, 1,
                  2, 4, 20, 11, 7, 4, 20, 39, 39))
    for case in cases:
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

    # linkedlist_test()
    distinct_linkedlist_test()

    print('py struct base demo done.')
