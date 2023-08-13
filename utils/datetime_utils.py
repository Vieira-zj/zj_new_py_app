# coding=utf-8
'''
Created on 2021-10-28

@author: zhengjin
'''

import datetime
import time
import traceback
from datetime import datetime as dt


def get_current_date() -> str:
    # datetime.date object -> str
    return str(dt.now().date())


def get_date_by_delta_days(input_date: str, delta_days: int) -> str:
    if delta_days == 0:
        return input_date

    input_dt = dt.strptime(input_date, '%Y-%m-%d')
    ret_dt = None
    if delta_days > 0:
        ret_dt = input_dt + datetime.timedelta(days=delta_days)
    else:
        ret_dt = input_dt - datetime.timedelta(days=abs(delta_days))
    return str(ret_dt.date())


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


def get_deltatime_milliseconds(delta):
    return delta.seconds * 1000 + int(delta.microseconds / 1000)


def test_duration_by_datetime():
    start = dt.now()
    time.sleep(2.3)
    duration = dt.now() - start
    print('duration seconds:', duration.seconds)
    print('duration seconds: %.2f' % duration.total_seconds())
    print('duration milliseconds:', get_deltatime_milliseconds(duration))


if __name__ == '__main__':

    try:
        # print(get_current_date())
        # print(get_date_by_delta_days('2022-03-14', 14))
        # print(get_date_by_delta_days(get_current_date(), 4))

        # print(get_delta_days('2021-10-18', '2021-10-30'))
        # print(get_week_of_year_v1('2021-12-23'))
        # print(get_week_of_year_v2('2021-12-23'))

        # print(format_timestamp_to_datetime(time.time()))
        # print(format_timestamp_to_datetime('1635416838'))
        # print(format_datetime_to_timestamp('2021-10-18 20:05:43'))

        test_duration_by_datetime()
    except:
        traceback.print_exc()

    print('datetime test done')
