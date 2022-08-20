# coding=utf-8
import base64
import json
from typing import List, Dict, Union, Callable


"""
raw data by sql:

select pay_load from replay_invocation_tab
where entrance = 1 and start_at between 1658332800000 and 1658419200000
order by app_name, identity;
"""


def parse_replay_invocations_tab_data(in_path: str, out_path: str):
    apppath_reqs_dict: Dict[str, list] = {}
    with open(in_path) as in_file:
        for line in in_file.readlines():
            row = json.loads(line)
            row_id = f"{row['app_name']}||{row['identity']}"
            reqs = apppath_reqs_dict.get(row_id, [])
            reqs.append(build_request(row['request']))
            apppath_reqs_dict[row_id] = reqs

    apppath_groupby_reqs_dict: Dict[str, dict] = {}
    for k, reqs in apppath_reqs_dict.items():
        reqs = sorted(reqs, key=lambda x: len(x))
        # apppath_groupby_reqs_dict[k] = groupby_requests(
        #     reqs, is_dict_equal_by_field)
        apppath_groupby_reqs_dict[k] = groupby_requests(
            reqs, is_dict_equal_by_value)

    app_dict: Dict[str, list] = {}
    for k, v in apppath_groupby_reqs_dict.items():
        app_name, path = k.split('||')
        for req, count in v.items():
            vals = app_dict.get(app_name, [])
            vals.append((path, req, count))
            app_dict[app_name] = vals

    app_sortby_count_dict: Dict[str, list] = {}
    for k, v in app_dict.items():
        sorted_v = sorted(v, key=lambda x: x[2], reverse=True)
        app_sortby_count_dict[k] = sorted_v

    with open(out_path, mode="w") as out_file:
        for k, vals in app_sortby_count_dict.items():
            for val in vals:
                path, req, count = val
                line = f'{k}||{path}||{req}||{count}\n'
                out_file.write(line)


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
    cur_req = reqs[0]
    count = 1
    for req in reqs[1:]:
        if compare_fn(cur_req, req):
            count += 1
        else:
            ret_dict[dump_request(cur_req)] = count
            cur_req = req
            count = 1
    ret_dict[dump_request(cur_req)] = count
    return ret_dict


def dump_request(obj: Union[dict, str]) -> str:
    try:
        return json.dumps(obj)
    except:
        return obj


def is_dict_equal_by_field(d1, d2) -> bool:
    """
    Only compare fields of 1st level.
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


def sort_dict_by_value(d: dict, is_reverse: bool = False) -> dict:
    lst = sorted(d.items(), key=lambda x: x[1], reverse=is_reverse)
    res = {k: v for k, v in lst}
    return res


def main():
    in_path = '/tmp/test/sql_space/sql_dump.txt'
    out_path = '/tmp/test/sql_space/sql_dump_out.txt'
    parse_replay_invocations_tab_data(in_path, out_path)


if __name__ == '__main__':

    # d = {'four': 4, 'one': 1, 'three': 3, 'two': 2}
    # print(sort_dict_by_value(d))

    # d1 = {"sp_uid": 1230, "data": {"token": "xyz",  "bu": "cn"}}
    # d2 = {"sp_uid": 1231, "data": {"token": "abc",  "bu": "sg"}}
    # print(is_dict_equal_by_value(d1, d2))

    main()
    print('parse done')
