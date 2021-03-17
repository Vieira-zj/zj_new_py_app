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


def bin_search01(val: int, sort_list: list, start: int, end: int) -> int:
    '''
    二分查找 有序数组 O(logN) 递归
    '''
    if start > end:
        return -1

    mid = int(start + (end - start) / 2)
    if val > sort_list[mid]:
        return bin_search01(val, sort_list, mid+1, end)
    elif val < sort_list[mid]:
        return bin_search01(val, sort_list, start, mid-1)
    else:
        return mid


def bin_search02(val: int, sort_list: list) -> int:
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
    for val in (1, 12, 77):
        print('#1. search number %d, and index %d' %
              (val, bin_search01(val, numbers, 0, len(numbers)-1)))
        print('#2. search number %d, and index %d' %
              (val, bin_search02(val, numbers)))


if __name__ == '__main__':

    test03()
    print('py alg sort demo done.')
