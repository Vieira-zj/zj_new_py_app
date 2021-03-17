# coding: utf-8

class TestMeta(object):

    def __init__(self, title='default-title', run_type='http', priority=2):
        self._title = title
        self._run_type = run_type
        self._priority = priority

    @property
    def title(self):
        return self._title

    @property
    def run_type(self):
        return self._run_type

    @property
    def priorityNumber(self) -> int:
        return self._priority

    @property
    def priority(self) -> str:
        if self._priority == 1:
            return 'high'
        elif self._priority == 2:
            return 'mid'
        else:
            return 'low'

    def to_string(self):
        return f"title={self.title},run_type={self.run_type},priority={self.priority}"


def test_meta(meta_object):
    ''' @test_meta '''

    def _deco(func):
        func.test_meta = meta_object
        return func

    return _deco


def test_desc(desc: str):
    ''' @test_desc '''

    def _deco(func):
        func.test_desc = desc
        return func

    return _deco


if __name__ == '__main__':

    pass
