# coding=utf-8
'''
Created on 2021-10-28

@author: zhengjin
'''

import time
import datetime
import traceback

from datetime import datetime as dt


def get_current_date() -> str:
    # datetime.date object -> str
    now = dt.now()
    return dt.strftime(now, '%Y-%-m-%-d')


def get_date_by_next_days(input_date: str, next_days: int) -> str:
    formater = '%Y-%m-%d'
    dt_obj = dt.strptime(input_date, formater)
    next_dt_obj = dt_obj + datetime.timedelta(days=next_days)
    return next_dt_obj.strftime(formater)


def get_delta_days(old_date: str, new_date: str) -> int:
    # str -> datetime.date object
    old_dt = dt.strptime(old_date, '%Y-%m-%d')
    new_dt = dt.strptime(new_date, '%Y-%m-%d')
    delta = new_dt - old_dt
    return delta.days


def get_week_of_year_v1(input_date: str) -> str:
    dt_obj = dt.strptime(input_date, '%Y-%m-%d')
    return dt.strftime(dt_obj, '%Y-%V')


def get_week_of_year_v2(input_date: str) -> str:
    """
    input_date: 2021-10-18
    """
    items = [int(item) for item in input_date.split('-')]
    calendar = datetime.date(*items).isocalendar()
    return f'{calendar[0]}-{calendar[1]}'


def format_timestamp_to_datetime(input_ts: str) -> str:
    if len(input_ts) == 13:
        input_ts = input_ts[:-3]
    return dt.fromtimestamp(int(input_ts)).strftime("%Y-%m-%d %H:%M:%S")


def format_datetime_to_timestamp(input_datetime) -> int:
    """
    input_datetime: 2021-10-18 20:05:43
    """
    d = dt.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(d.timetuple()))


if __name__ == '__main__':

    try:
        # print(get_current_date())
        # print(get_date_by_next_days('2021-10-28', 4))

        # print(get_delta_days('2021-10-18', '2021-10-30'))
        # print(get_week_of_year_v1('2021-12-23'))
        # print(get_week_of_year_v2('2021-12-23'))

        # print(format_timestamp_to_datetime(time.time()))
        print(format_timestamp_to_datetime('1635416838'))
        # print(format_datetime_to_timestamp('2021-10-18 20:05:43'))
    except:
        traceback.print_exc()

    print('datetime test done')
