# coding=utf-8

def desc(desc):
    """ @desc: a testcase description. """

    def _deco(func):
        func.desc = desc
        return func

    return _deco


class TestSuite01(object):

    @desc('testcase01 in testsuite01')
    def test_case01(self):
        print('run testCase01')

    @desc('testcase02 in testsuite01')
    def test_case02(self):
        print('run testCase02')

    def testsuite_desc(self):
        print('testsuite01 includes 2 test cases.')


class TestSuite02(object):

    @desc('testcase11 in testsuite02')
    def test_case11(self):
        print('run testCase11')

    def test_case12_skip(self):
        print('run testCase12')
