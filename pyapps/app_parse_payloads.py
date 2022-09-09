# coding=utf-8

import base64
import functools
import json
from typing import List, Dict, Union, Callable


"""
raw data by sql:
select pay_load from replay_invocation_tab
where entrance = 1 and start_at between 1658332800000 and 1658419200000
order by app_name, identity;

payload fields:
app_name, identity, request
"""

is_debug = True


def parse_payloads_data(in_path: str, out_path: str):
    # row: {"app1||path1":[req11{},req12{}...], "app2||path2":[req21{},req22{}...]}
    apppath_to_reqs_dict: Dict[str, list] = {}
    for line in load_payloads(in_path, is_mock=is_debug):
        row = json.loads(line)
        row_key = f"{row['app_name']}||{row['identity']}"
        reqs = apppath_to_reqs_dict.get(row_key, [])
        reqs.append(build_request(row['request']))
        apppath_to_reqs_dict[row_key] = reqs

    # row: {"app1||path1":{"req11":1,"req12":2}, "app2||path2":{"req21":6,"req22":3}}
    apppath_to_groupby_reqs_dict: Dict[str, dict] = {}
    for k, reqs in apppath_to_reqs_dict.items():
        apppath_to_groupby_reqs_dict[k] = groupby_requests(
            reqs, is_dict_equal_by_field)
        # apppath_to_groupby_reqs_dict[k] = groupby_requests(
        #     reqs, is_dict_equal_by_value)

    app_path_req_count_list: List[tuple] = []
    for k, v in apppath_to_groupby_reqs_dict.items():
        app_name, path = k.split('||')
        for req, count in v.items():
            item = (app_name, path, req, count)  # use tuple
            app_path_req_count_list.append(item)

    cmp_key = functools.cmp_to_key(payloads_compare)
    sorted_app_path_req_count_list = sorted(
        app_path_req_count_list, key=cmp_key)

    out_lines = []
    for item in sorted_app_path_req_count_list:
        app_name, path, req, count = item
        line = f'{app_name}||{path}||{req}||{count}\n'
        out_lines.append(line)
    dump_payloads(out_path, out_lines, is_mock=is_debug)


def build_request(request: str) -> Union[dict, str]:
    if len(request) == 0:
        return {}

    req = base64.b64decode(request).decode()
    try:
        return json.loads(req)
    except:
        return req


def groupby_requests(reqs: list, compare_fn: Callable) -> Dict[str, int]:
    ret_dict = {}
    while True:
        if len(reqs) == 0:
            return ret_dict

        cur_req = reqs[0]
        cur_req_str = dump_request(reqs[0])
        ret_dict[cur_req_str] = 1
        if len(reqs) == 1:
            return ret_dict

        not_matched_reqs = []
        for req in reqs[1:]:
            if is_dict_equal_by_field(cur_req, req):
                ret_dict[cur_req_str] += 1
            else:
                not_matched_reqs.append(req)
        reqs = not_matched_reqs


def dump_request(obj: Union[dict, str]) -> str:
    try:
        return json.dumps(obj)
    except:
        return obj


def is_dict_equal_by_field(d1, d2) -> bool:
    """
    Only compare 1st level fields of dict.
    """
    if type(d1) != type(d2) or len(d1) != len(d2):
        return False

    try:
        for k in d1.keys():
            if k not in d2.keys():
                return False
        return True
    except:
        return d1 == d2


def is_dict_equal_by_value(d1, d2) -> bool:
    try:
        for k, v in d1.items():
            if is_key_skip_by_whitelist(k):
                continue
            if isinstance(v, dict):
                return is_dict_equal_by_value(v, d2[k])
            if d2[k] != v:
                return False
        return True
    except:
        return False


def is_key_skip_by_whitelist(val: str) -> bool:
    for tag in ('id', 'token', 'timestamp', 'signature'):
        if tag in val:
            return True
    return False


def payloads_compare(x: tuple, y: tuple) -> int:
    x_app, x_path, _, x_count = x
    y_app, y_path, _, y_count = y
    if x_app != y_app:
        return 1 if x_app > y_app else -1
    if x_count != y_count:
        return y_count - x_count
    if x_path != y_path:
        return 1 if x_path > y_path else -1
    return 1


def load_payloads(in_path: str, is_mock: bool = False) -> list:
    if is_mock:
        return [
            '{"app_name":"app_test","identity":"/query","request":"eyJtc2ciOiJpdHMgdGVzdCJ9Cg=="}',
            '{"app_name":"app_hello","identity":"/index","request":"eyJtc2ciOiJoZWxsb3dvcmxkIn0K"}',
            '{"app_name":"app_hello","identity":"/ping","request":"eyJtc2ciOiJwaW5nIn0K"}',
            '{"app_name":"app_hello","identity":"/index","request":"eyJtc2ciOiJoZWxsb3dvcmxkIn0K"}',
            '{"app_name":"app_hello","identity":"/index","request":"eyJtc2ciOiJoZWxsb3dvcmxkIn0K"}',
            '{"app_name":"app_hello","identity":"/ping","request":"eyJtc2ciOiJwaW5nIn0K"}',
            '{"app_name":"app_hello","identity":"/index","request":"eyJtc2ciOiJoZWxsb3dvcmxkIn0K"}',
            '{"app_name":"app_hello","identity":"/ping","request":"eyJtc2ciOiJwaW5nIn0K"}',
        ]

    with open(in_path) as in_file:
        return in_file.readlines()


def dump_payloads(out_path: str, out_lines: List[str], is_mock: bool = False):
    if is_mock:
        for line in out_lines:
            print(line)
        return

    with open(out_path, mode="w") as out_file:
        for line in out_lines:
            out_file.write(line)


def main():
    in_path = '/tmp/test/sql_space/sql_dump.txt'
    out_path = '/tmp/test/sql_space/sql_dump_out.txt'
    parse_payloads_data(in_path, out_path)


if __name__ == '__main__':

    reqs = [
        {"uid": 1221654048},
        {"uid": 1221654049},
        {"otp_token": "111111"},
        {"uid": 1221654050},
        {"sp_uid": 1221724968},
        {"uid": 1221654051},
        {"sp_uid": 1221724967},
    ]
    res = groupby_requests(reqs, is_dict_equal_by_field)
    for k, v in res.items():
        print(k, v)

    # d1 = {"sp_uid": 1230, "data": {"token": "xyz",  "bu": "cn"}}
    # d2 = {"sp_uid": 1231, "data": {"token": "abc",  "bu": "sg"}}
    # print(is_dict_equal_by_field(d1, d2))
    # print(is_dict_equal_by_value(d1, d2))

    # d = {'four': 4, 'one': 1, 'three': 3, 'two': 2}
    # print(sort_dict_by_value(d))

    # main()
    print('payfload parse done')
