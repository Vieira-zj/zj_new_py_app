# coding=utf-8

def is_palindrome(input: str) -> bool:
    """
    验证回文串
    给定一个字符串，验证它是否是回文串，只考虑字母和数字字符，可以忽略字母的大小写。
    """
    start = 0
    end = len(input) - 1
    while start < end:
        while (not input[start].isalnum()) and (start < end):
            start += 1
        while (not input[end].isalnum()) and (start < end):
            end -= 1
        if input[start].lower() != input[end].lower():
            return False
        start += 1
        end -= 1
    return True


def test_is_palindrome():
    test_data = (
        ('A man, a plan, a canal: Panama', True),
        ('race a car', False)
    )
    for input, want in test_data:
        got = is_palindrome(input)
        assert got == want, f'got {got}, want {want}'


def two_sum(nums: list, target: int) -> list:
    """
    两数之和
    给定一个整数数组 nums 和一个目标值 target, 请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
    """
    tmp_d = {}
    for idx, num in enumerate(nums):
        res = target - num
        if res in tmp_d.keys():
            return [tmp_d[res], idx]
        tmp_d[num] = idx


def test_two_sum():
    test_data = (
        ([2, 7, 11, 15], 9),
        ([-3, 4, 90, 3], 0),
    )
    for nums, target in test_data:
        res = two_sum(nums, target)
        print(res)


if __name__ == '__main__':

    test_two_sum()
