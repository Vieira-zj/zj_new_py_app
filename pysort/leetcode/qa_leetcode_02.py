# coding=utf-8

def single_sumber(nums: list):
    """
    只出现一次的数字
    给定一个非空整数数组，除了某个元素只出现 1 次以外，其余每个元素均出现 2 次。找出那个只出现了 1 次的元素。

    1 ^ 0 = 1
    1 ^ 1 = 0
    """
    base = nums[0]
    for num in nums[1:]:
        base ^= num
    return base


def test_single_sumber():
    test_data = (
        ([2, 2, 1], 1),
        ([4, 1, 2, 1, 2], 4),
    )
    for nums, want in test_data:
        res = single_sumber(nums)
        assert res == want, f'want {want}, got {res}'


def majority_element(nums: list):
    """
    多数元素
    给定一个大小为 n 的数组，找到其中的多数元素。多数元素是指在数组中出现次数大于 [ n/2 ] 的元素。
    """
    group = count = 0
    for num in nums:
        if count == 0:
            group = num
            count += 1
            continue
        if num == group:
            count += 1
        else:
            count -= 1
    return group


def test_majority_element():
    test_data = (
        ([3, 3, 4], 3),
        ([2, 2, 1, 1, 4, 2, 2], 2)
    )
    for nums, want in test_data:
        got = majority_element(nums)
        assert got == want, f'want {want}, got {got}'


def move_zeroes(input: list):
    """
    移动零
    将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
    """
    # 非零数字前移
    cur = 0
    for ch in input:
        if ch != 0:
            input[cur] = ch
            cur += 1
    for i in range(cur, len(input)):
        input[i] = 0


def test_move_zeroes():
    test_data = (
        [0, 1, 0, 3, 12],
    )
    for input in test_data:
        move_zeroes(input)
        print(input)


if __name__ == '__main__':

    test_move_zeroes()
