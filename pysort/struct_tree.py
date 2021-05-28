# coding=utf-8

import sys
import os

sys.path.append(os.getenv('PYROOT'))
from pysort import Stack, StackEmptyException


# -----------------------------------
# 二叉树
# -----------------------------------


class BinTreeNode(object):

    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None

    def Left(self, node):
        self.left = node

    def Right(self, node):
        self.right = node


def create_bin_tree(in_list: list) -> BinTreeNode:
    nodes = []
    for i in range(0, len(in_list)):
        nodes.append(BinTreeNode(i))

    for i in range(0, int(len(nodes) / 2)):
        nodes[i].Left(nodes[i*2 + 1])
        if i*2 + 2 < len(nodes):
            nodes[i].Right(nodes[i*2 + 2])
    return nodes[0]

# -----------------------------------
# Tree Iterator
# -----------------------------------


def pre_order_bin_tree01(root: BinTreeNode):
    '''
    按层打印二叉树 从上往下 从左往右（先序遍历-递归）
    '''
    if root is None:
        return
    print(root.value, end='')
    pre_order_bin_tree01(root.left)
    pre_order_bin_tree01(root.right)


def pre_order_bin_tree02(root):
    '''
    按层打印二叉树 从上往下 从左往右（先序遍历-非递归）
    '''
    s = Stack()
    s.push(root)
    try:
        while True:
            node = s.pop()
            print(node.value, end='')
            if node.right != None:
                s.push(node.right)
            if node.left != None:
                s.push(node.left)
    except StackEmptyException as e:
        print('\n', e)


def pre_order_bin_tree_test():
    bin_tree = create_bin_tree(range(0, 10))
    print('#1. print bin tree by pre order:')
    pre_order_bin_tree01(bin_tree)
    print()

    print('#2. print bin tree by pre order:')
    pre_order_bin_tree02(bin_tree)


def get_tree_max_depth(root: BinTreeNode) -> int:
    '''
    树的最大深度
    '''
    if root is None:
        return 0

    l_depth = get_tree_max_depth(root.left) + 1
    r_depth = get_tree_max_depth(root.right) + 1
    return max(l_depth, r_depth)


def get_tree_max_depth_test():
    bin_tree = create_bin_tree(range(0, 10))
    print('max tree depth:', get_tree_max_depth(bin_tree))


if __name__ == '__main__':

    # pre_order_bin_tree_test()
    get_tree_max_depth_test()
    print('py struct tree demo done.')
