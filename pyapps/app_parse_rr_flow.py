# coding=utf-8
import base64
import json
from typing import List, Dict, Union


"""
raw data by sql:

select distinct pay_load
from replay_invocation_tab
where entrance = 1 and start_at between 1658332800000 and 1658419200000
order by app_name, identity;
"""


def parse_replay_invocations_tab_data(in_path: str, out_path: str):
    dicts: Dict[str, list] = {}
    with open(in_path) as in_file:
        for line in in_file.readlines():
            row = json.loads(line)
            row_id = f"{row['app_name']}|{row['identity']}"
            reqs = dicts.get(row_id, [])
            req = build_request(row['request'])
            reqs.append(req)
            dicts[row_id] = reqs

    res_dicts: Dict[str, dict] = {}
    for k, reqs in dicts.items():
        reqs = sorted(reqs, key=lambda x: len(x))
        res_dicts[k] = group_requests_by_field(reqs)
        # res_dicts[k] = group_requests_by_value(reqs)

    with open(out_path, mode="w") as out_file:
        for k, v in res_dicts.items():
            for req, count in v.items():
                line = f'{k}|{req}|{count}\n'
                out_file.write(line)


def build_request(request: str) -> Union[dict, str]:
    if len(request) == 0:
        return {}

    req = base64.b64decode(request).decode()
    try:
        return json.loads(req)
    except:
        return req


def group_requests_by_field(reqs: list) -> Dict[str, int]:
    """
    group requests only fields are equal, not compare values.
    """
    ret_dicts = {}
    cur_req = reqs[0]
    count = 1
    for req in reqs[1:]:
        if is_dict_equal_by_field(req, cur_req):
            count += 1
        else:
            ret_dicts[dump_request(cur_req)] = count
            cur_req = req
            count = 1
    ret_dicts[dump_request(cur_req)] = count
    return ret_dicts


def group_requests_by_value(reqs: list) -> Dict[str, int]:
    """
    group requests which str are equal.
    """
    ret_dicts = {}
    for req in reqs:
        req_str = dump_request(req)
        count = ret_dicts.get(req_str, 0)
        ret_dicts[req_str] = count + 1
    return ret_dicts


def dump_request(obj: Union[dict, str]) -> str:
    try:
        return json.dumps(obj)
    except:
        return obj


def is_dict_equal_by_field(d1, d2) -> bool:
    if type(d1) != type(d2) or len(d1) != len(d2):
        return False

    try:
        for k in d1.keys():
            if k not in d2.keys():
                return False
        return True
    except:
        return d1 == d2


def main():
    in_path = '/tmp/test/sql_space/sql_dump.txt'
    out_path = '/tmp/test/sql_space/sql_dump_out.txt'
    parse_replay_invocations_tab_data(in_path, out_path)


if __name__ == '__main__':

    # print(is_dict_equal_by_field({}, {}))
    main()
    print('parse done')
