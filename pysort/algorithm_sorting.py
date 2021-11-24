# -*- coding: utf-8 -*-
'''
Created on 2019-11-08
@author: zhengjin
'''

# -----------------------------------
# Sort
# -----------------------------------


def bubble_sort(iter: list):
    '''
    冒泡排序（交换排序）O(N*N)
    '''
    size = len(iter)
    for i in range(size - 1):
        is_exchange = False
        for j in range(size - 1 - i):
            if iter[j] > iter[j + 1]:
                iter[j], iter[j + 1] = iter[j + 1], iter[j]
                is_exchange = True
        if not is_exchange:
            return


def test01():
    numbers = [15, 16, 1, 99, 50, 0, 99, 13, 6, 2]
    bubble_sort(numbers)
    print('bubble sort results:', numbers)


def quick_sort(iter: list, start: int, end: int):
    '''
    快速排序（交换排序）O(N*logN)
    '''
    if start >= end:
        return

    mid = iter[start]
    left = start  # error: left = start + 1
    right = end

    while (left < right):
        while left < right and iter[right] >= mid:
            right -= 1
        while left < right and iter[left] <= mid:
            left += 1
        if left < right:
            iter[left], iter[right] = iter[right], iter[left]

    # 从右开始往左移动 当left=right时 指向比mid小的数
    iter[start] = iter[left]
    iter[left] = mid

    quick_sort(iter, start, left - 1)
    quick_sort(iter, left + 1, end)


def test02():
    numbers = [15, 16, 1, 7, 99, 50, 0, 99, 13, 7]
    quick_sort(numbers, 0, len(numbers) - 1)
    print('quick sort results:', numbers)


def merge_sort(iter: list) -> list:
    '''
    归并排序 O(N*logN)
    '''
    if len(iter) == 1:
        return iter

    mid = int(len(iter) / 2)
    iter1 = merge_sort(iter[:mid])
    iter2 = merge_sort(iter[mid:])
    return merge(iter1, iter2)


def merge(iter1: list, iter2: list) -> list:
    ret_iter = []
    i = j = 0
    while i < len(iter1) and j < len(iter2):
        if iter1[i] < iter2[j]:
            ret_iter.append(iter1[i])
            i += 1
        else:
            ret_iter.append(iter2[j])
            j += 1

    return (ret_iter + iter1[i:]) if i < len(iter1) else (ret_iter + iter2[j:])


def test03():
    numbers = [3, 16, 14, 8, 99, 53, 0, 99, 8, 32, 66]
    print('merge sort results:', merge_sort(numbers))

# -----------------------------------
# Search
# -----------------------------------


def bin_search01(val: int, sort_list: list) -> int:
    """
    二分查找 有序数组 O(logN) 递归
    问题：有 list 复制操作，效率较差
    """
    if len(sort_list) == 1:
        return sort_list[0] == val

    pos = int(len(sort_list) / 2)
    if sort_list[pos] == val:
        return True

    if val < sort_list[pos]:
        return bin_search01(val, sort_list[:pos])
    else:
        return bin_search01(val, sort_list[pos:])


def bin_search02(val: int, sort_list: list, start: int, end: int) -> int:
    '''
    二分查找 有序数组 O(logN) 递归
    '''
    if start > end:
        return -1

    mid = int(start + (end - start) / 2)
    if val > sort_list[mid]:
        return bin_search02(val, sort_list, mid+1, end)
    elif val < sort_list[mid]:
        return bin_search02(val, sort_list, start, mid-1)
    else:
        return mid


def bin_search03(val: int, sort_list: list) -> int:
    '''
    二分查找 有序数组 O(logN) 非递归
    '''
    start = 0
    end = len(sort_list) - 1

    while start <= end:
        mid = int(start + (end - start) / 2)
        if val > sort_list[mid]:
            start = mid + 1
        elif val < sort_list[mid]:
            end = mid - 1
        else:
            return mid
    return -1


def test04():
    numbers = [1, 3, 4, 6, 8, 9, 10, 12, 13, 77]
    for val in (1, 12, 77, 100):
        print('search number %d, and result %s' %
              (val, bin_search01(val, numbers)))
        # print('search number %d, and index %d' %
        #       (val, bin_search02(val, numbers, 0, len(numbers)-1)))
        # print('search number %d, and index %d' %
        #       (val, bin_search03(val, numbers)))

# -----------------------------------
# List Group By
# -----------------------------------


def list_group_by(src_list: list) -> list:
    '''
    element ui table 合并单元格
    '''
    for item in src_list:
        item['rowspan'] = 1
        item['colspan'] = 1
    sorted_list = sorted(src_list, key=lambda item: item['group'])

    i = 0
    while i < (len(sorted_list) - 1):
        cur_item = sorted_list[i]
        tmp_include = cur_item['include']
        while i < (len(sorted_list) - 1):
            next_item = sorted_list[i+1]
            if cur_item['group'] != next_item['group']:
                break
            cur_item['rowspan'] += 1
            next_item['include'] = []
            next_item['rowspan'] = 0
            next_item['colspan'] = 0
            tmp_include.extend(next_item['include'])
            i += 1

        if cur_item['rowspan'] > 0:
            cur_item['include'] = set(tmp_include)
        i += 1

    return sorted_list


def test05():
    src_list = [
        {'group': 'a', 'id': '01', 'include': [1, 2]},
        {'group': 'b', 'id': '02', 'include': [11, 13]},
        {'group': 'a', 'id': '07', 'include': [1, 3]},
        {'group': 'e', 'id': '10', 'include': [41, 43]},
        {'group': 'b', 'id': '03', 'include': [12, 13]},
        {'group': 'e', 'id': '05', 'include': [42, 43]},
        {'group': 'c', 'id': '08', 'include': [21, 23]},
        {'group': 'd', 'id': '09', 'include': [31, 32]},
        {'group': 'a', 'id': '04', 'include': [2, 4]},
        {'group': 'a', 'id': '06', 'include': [1, 4]},
    ]
    print('list group by, and and merge "include":')
    for item in list_group_by(src_list):
        print(item)


if __name__ == '__main__':

    test04()
    print('py alg sort demo done.')
