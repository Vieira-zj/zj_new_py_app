# coding=utf-8

from typing import List, Dict


class DiffEntry(object):
    def __init__(self, index, key, value):
        self.index = index
        self.key = key
        self.value = value
        self.dtype = ''

    def __str__(self):
        prefix = self.dtype if len(self.dtype) > 0 else self.index
        return f'[{prefix}]:{self.key}:{self.value}'


class JsonDictParser(object):
    def __init__(self):
        self.results: Dict[str, DiffEntry] = {}

    def parse(self, root_key: str, obj):
        if hasattr(obj, '__dict__'):
            # not happen: handle for class
            for k, v in vars(obj).items():
                pass
        elif 'dict' in str(type(obj)):
            for k, v in obj.items():
                key_path = k if len(root_key) == 0 else f'{root_key}:{k}'
                self.parse(key_path, v)
        elif 'list' in str(type(obj)):
            for i, item in enumerate(obj):
                self.parse(f'{root_key}[{i}]', item)
        elif 'str' in str(type(obj)) or 'int' in str(type(obj)):
            entry = DiffEntry(len(self.results), root_key, obj)
            self.results[root_key] = entry
        else:
            entry = DiffEntry(len(self.results), root_key, f'{obj}')
            self.results[root_key] = entry

    def get_results(self) -> Dict[str, DiffEntry]:
        return self.results


def json_diff(d1: dict, d2: dict) -> List[DiffEntry]:
    p = JsonDictParser()
    p.parse('', d1)
    res1 = p.get_results()
    print('json flat results1:')
    for val in res1.values():
        print(val)

    p = JsonDictParser()
    p.parse('', d2)
    res2 = p.get_results()
    print('json flat results2:')
    for val in res2.values():
        print(val)

    print('debug class:', type(p), hasattr(p, '__dict__'), vars(p).keys())

    results: List[DiffEntry] = []
    for key in set(res1.keys()).union(res2.keys()):
        if key not in res1.keys():
            entry = res2[key]
            entry.dtype = 'new'
            results.append(entry)
        elif key not in res2.keys():
            entry = res1[key]
            entry.dtype = 'null'
            results.append(entry)
        elif res1[key].value != res2[key].value:
            entry = res1[key]
            entry.dtype = 'diff'
            results.append(entry)
        else:
            pass

    return sorted(results, key=lambda item: item.key)


def test_json_diff():
    obj1 = {
        'code': 200,
        'msg': 'success',
        'total': 1,
        'data': [
            {
                'name': 'foo',
                'age': 30,
                'skill': ['java', 'python', 'golang'],
            },
        ],
    }
    obj2 = {
        'code': 201,
        'msg': 'success',
        'data': [
            {
                'name': 'bar',
                'age': 30,
                'skill': ['javascript', 'python'],
            },
        ],
        'comment': 'for test'
    }

    results = json_diff(obj1, obj2)
    print('\njson diff results:')
    for res in results:
        print(res)


if __name__ == '__main__':

    test_json_diff()
    print('json diff done')
