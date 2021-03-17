# -*- coding: utf-8 -*-
'''
Created on 2019-05-26
@author: zhengjin
'''

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


def pandas_series_demo01():
    # create series
    print('series with default index:\n', Series([1, 2, 3, 4]))  # 默认索引（从0到N-1）

    print('\nseries with index:\n', Series(
        range(4), index=['a', 'b', 'c', 'd']))

    dict_data = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
    print('\nseries by dict:\n', Series(dict_data))

    states = ['California', 'Ohio', 'Oregon', 'Texas']
    s = Series(dict_data, index=states)
    print('\nseries by dict and index:\n', s)
    print('\nseries in null:\n', pd.isnull(s))
    print('\nseries not null:\n', pd.notnull(s))


def pandas_series_demo02():
    # series index and value
    s = Series(range(4), index=['a', 'b', 'c', 'd'])
    print('series item at loc 0:', s[0])
    print('series item at idx "b":', s['b'])
    print('series item at idx "a" and "c":\n', s[['a', 'c']])

    print('\nseries index:\n', s.index.values)
    print('\nseries values:\n', s.values)


def pandas_series_demo03():
    # operation on series
    s = Series(range(4), index=['a', 'b', 'c', 'd'])
    print('series, items > 1:\n', s[s > 1])
    print('series, items * 2:\n', s * 2)
    print('square series:\n', np.square(s))
    print('series, sum by rows:\n', s.cumsum())

    # 相同索引值的元素相加
    dict_data = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
    s1 = Series(dict_data)
    states = ['California', 'Ohio', 'Oregon', 'Texas']
    s2 = Series(dict_data, index=states)
    s3 = s1 + s2
    print('\nseries1 + series2:\n', s3)

    s3.index.name = 'state'
    s3.name = 'population'
    print('\nseries with name:\n', s3)


def pandas_df_demo01():
    # create df
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    df = DataFrame(data_dict)
    print('dataframe:\n', df)
    col = df['year']
    print('\ncol type %s, and value:\n %s' % (type(col), col))
    row = df.iloc[0]
    print('\nrow type %s, and value:\n %s' % (type(row), row))

    cols = ['year', 'state', 'pop']
    print('\ndataframe by year:\n', DataFrame(data_dict, columns=cols))
    idx = ['1st', '2nd', '3rd', '4th', '5th']
    print('\ndataframe by index:\n', DataFrame(data_dict, index=idx))


def pandas_df_demo02():
    # create df
    data_dict = {
        'Nevada': {2001: 2.4, 2002: 2.9},
        'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6},
    }
    print('dataframe:\n', DataFrame(data_dict))

    idx = [2002, 2001, 2000]
    df = DataFrame(data_dict, index=idx)
    print('\ndataframe by index:\n', df)

    df.columns.name = 'state'
    df.index.name = 'year'
    print('\ndataframe by col and index:\n', df)


def pandas_df_demo03():
    # get df cols
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    df1 = DataFrame(data_dict)
    print('dataframe state:\n', df1['state'])
    print('\ndataframe population:\n', df1.year)

    # get df rows
    idx = ['one', 'two', 'three', 'four', 'five']
    df2 = DataFrame(data_dict, index=idx)
    print('\ndataframe row "one":\n', df2.loc['one'])
    print('\ndataframe row 2:\n', df2.iloc[1])

    rows = ['two', 'three', 'four']
    print('\ndataframe rows "two", "three", "four":\n', df2.loc[rows])
    print('\ndataframe row 1~3:\n', df2.iloc[range(3)])


def pandas_df_demo04():
    # get df cell
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    idx = ['one', 'two', 'three', 'four', 'five']
    df = DataFrame(data_dict, index=idx)
    print('dataframe:\n', df)

    # index by [col,row]
    print('\ndataframe row 1 state:', df['state'][0])
    print('dataframe row two pop:', df['pop']['two'])
    # index by [row, col]
    print('\ndataframe row 1 state:', df.iloc[0]['state'])
    print('dataframe row two pop:', df.loc['two']['pop'])


def pandas_df_demo05():
    # update df
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    idx = ['one', 'two', 'three', 'four', 'five']
    df = DataFrame(data_dict, index=idx)

    df['debt'] = 10
    print('add col debt dataframe:\n', df)
    df['debt'] = np.arange(5)
    print('\nupdate col debt dataframe:\n', df)

    east = (df['state'] == 'Ohio')
    df['east'] = east
    print('\nadd col east dataframe:\n', df)


def pandas_df_demo06():
    # 1
    df = DataFrame(np.arange(9).reshape(3, 3),
                   index=['bj', 'sh', 'gz'], columns=['a', 'b', 'c'])
    print('dataframe:\n', df)

    df.index = Series(['beijing', 'shanghai', 'guangzhou'])
    print('\nupdate index df:\n', df)
    df.index = df.index.map(str.upper)
    print('\nupdate index with upper df:\n', df)

    df1 = df.rename(index=str.lower, columns=str.upper)
    print('\nupdate index and cols df:\n', df1)

    # 2
    df2 = DataFrame([
        [2.0, 1.0, 3.0, 5],
        [3.0, 4.0, 5.0, 5],
        [3.0, 4.0, 5.0, 5],
        [1.0, 0.0, 6.0, 5]],
        columns=list('abcd'))
    print('\nsum by rows df:\n', df2.cumsum(axis=0))  # default
    print('\nsum by cols df:\n', df2.cumsum(axis=1))


def pandas_df_demo07():
    # function: pd.cut()
    np.random.seed(666)

    # 1
    score_list = np.random.randint(25, 100, size=20)
    print('scores:', score_list)

    partitions = [0, 59, 70, 80, 100]
    labels = ['low', 'middle', 'good', 'perfect']
    score_cut = pd.cut(score_list, partitions, labels=labels)
    print('category scores:\n', score_cut)
    print('\ncategory count:\n', pd.value_counts(score_cut))

    # 2
    df = DataFrame()
    df['score'] = score_list
    df['student'] = [pd.util.testing.rands(3) for i in range(len(score_list))]
    print('\nstudents and scores df:\n', df)

    df['category'] = pd.cut(df['score'], partitions, labels=labels)
    print('\nstudents and scores by category df:\n', df)

    # save to csv
    df.index.name = 'idx'
    save_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files', 'test.out')
    df.to_csv(save_path)


def pandas_df_demo08():
    # np.dtype高效地存储数据
    mem = pd.DataFrame([[133, 2, 4]], columns=[
                       'uid', 'dogs', 'cats']).memory_usage()
    print('default int64 memory usage:\n', mem)

    mem = pd.DataFrame([[133, 2, 4]], columns=['uid', 'dogs', 'cats']) \
        .astype({
            'uid': np.dtype('int32'),
            'dogs': np.dtype('int32'),
            'cats': np.dtype('int32')
        }).memory_usage()
    print('\ndefault int32 memory usage:\n', mem)


def pandas_df_demo09():
    # axis=0 沿着行方向（纵向）, axis=1 沿着列方向（横向）
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': [1, 2, 3],
        'col3': [1, 2, 3],
    })
    print('df data:\n', df)

    df1 = df.drop('col2', axis=1)
    print('\ndrop col2, and df data:\n', df1)
    df2 = df.drop(1, axis=0)
    print('\ndrop row2, and df data:\n', df2)

    avg1 = df.mean(axis=1)
    print('\navg value for each line:\n', avg1)
    avg2 = df.mean(axis=0)
    print('\navg value for each row:\n', avg2)


def pandas_df_demo10():
    df = pd.DataFrame(np.arange(9).reshape(3, 3), columns=[
                      'col1', 'col2', 'col3'], index=['one', 'two', 'three'])
    df['col4'] = df.apply(lambda x: x.sum(), axis=1)
    print('sum of each row:\n', df)

    total = df.apply(lambda x: x.sum(), axis=0)
    df.loc['total'] = total
    print('\nsum of each col:\n', df)


def pandas_df_demo11():
    rand = np.random.RandomState(66)
    dframe = pd.DataFrame(rand.randint(100, size=(4, 3)), columns=list(
        'bde'), index=['India', 'USA', 'China', 'Russia'])
    print(dframe)

    print('\nmap for each value')
    def changefn(x): return '%.2f' % x
    print(dframe['d'].map(changefn))

    print('\napply for each series')
    def fn(x): return x.max() - x.min()
    print(dframe.apply(fn))

    print('\nisin 过滤数据帧')
    cond = dframe['e'].isin([90, 74])
    print(dframe[cond])

    print('\npivot_table 数据透视表 (instead of groupby)')
    school = pd.DataFrame({
        'A': ['Jay', 'Usher', 'Nicky', 'Romero', 'Will'],
        'B': ['Masters', 'Graduate', 'Graduate', 'Masters', 'Graduate'],
        'C': [26, 22, 20, 23, 24]})
    print(school)
    print()

    # 根据年龄和课程来创建数据透视表
    table = pd.pivot_table(school, values='A', index=['B', 'C'],
                           columns=['B'], aggfunc=np.sum, fill_value='Not Available')
    print(table)


def pandas_df_pipeline():
    def load_df():
        file_path = get_lemon_cases_excel_path()
        return pd.read_excel(file_path, sheet_name='Sheet1', parse_dates=['birthdate'])

    def check_df(df):
        cols = ['income', 'outcome']
        cond = df[cols].isna().any(axis=1)
        return df[cond]

    def cal_split_mail(x_df):
        def split_mail(x_s):
            arr = x_s.split('@')
            prefix = arr[0]
            post = arr[1]
            return Series((prefix, post), index='mail_prefix mail_post'.split())

        res = x_df['mail'].apply(split_mail)
        x_df[res.columns] = res
        return x_df

    def cal_convert_sex(x_df):
        mapping = {'M': '男', 'F': '女'}
        x_df['sex'] = x_df['sex'].map(mapping)
        return x_df

    df = load_df()
    print('load df:\n', df)
    df = check_df(df)
    print('\ncheck df and invalid data:\n', df)

    res = (load_df().pipe(cal_split_mail).pipe(cal_convert_sex))
    print('\npipeline df:\n', res)


def pandas_plot_demo01():
    # series.plot()
    np.random.seed(666)
    s1 = Series(np.random.randn(1000)).cumsum()
    s2 = Series(np.random.randn(1000)).cumsum()

    show_num = 3
    if show_num == 1:
        s1.plot(kind='line', grid=True, label='S1', title='series_s1')
        s2.plot(label='s2')
    elif show_num == 2:
        figure, ax = plt.subplots(2, 1)
        ax[0].plot(s1)
        ax[1].plot(s2)
    elif show_num == 3:
        fig, ax = plt.subplots(2, 1)
        s1.plot(ax=ax[1], label='s1')
        s2.plot(ax=ax[0], label='s2')
    else:
        raise KeyError('invalid show_num!')

    plt.legend()
    plt.show()


def pandas_plot_demo02():
    # dataframe.plot()
    np.random.seed(666)
    df = DataFrame(np.random.randint(1, 20, size=40).reshape(10, 4),
                   columns=['a', 'b', 'c', 'd'])

    show_num = 3
    if show_num == 1:
        # 柱状图
        df.plot(kind='bar')
    elif show_num == 2:
        # 横向的柱状图
        df.plot(kind='barh')
    elif show_num == 3:
        for i in df.index:
            df.iloc[i].plot(label='row' + str(i))
        plt.legend()
    else:
        raise KeyError('invalid show_num!')

    plt.show()


def pandas_df_save_demo():
    data_dict = {
        'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9],
    }
    dir_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')

    # save as csv
    df1 = DataFrame(data_dict, index=range(1, 6))
    print('dataframe to be saved as csv:\n', df1)
    df1.to_csv(os.path.join(dir_path, 'test_df.csv'))

    # save as parquet
    # pre-condition: pip3 install fastparquet
    pd.show_versions()

    df2 = DataFrame(data_dict)
    print('\ndataframe to be saved as parquet:\n', df2)
    # df2.to_parquet(os.path.join(dir_path, 'test_df.parquet.gzip'))
    # RuntimeError: Compression 'snappy' not available. Options: ['GZIP', 'UNCOMPRESSED']
    df2.to_parquet(os.path.join(dir_path, 'test_df.parquet.gzip'),
                   engine='fastparquet', compression='gzip')


def pandas_df_read_demo():
    home_dir = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files')

    # read csv
    csv_path = os.path.join(home_dir, 'test_df.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, index_col=0)
        print('read from csv, dataframe:\n', df)

    # read parquet
    file_path = os.path.join(home_dir, 'test_df.parquet.gzip')
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path, engine='fastparquet')
        print('read from parquet, dataframe:\n', df)

    # read parquet(hive)
    file_path = os.path.join('/tmp/hive_test', 'pokes_0.parquet')
    if os.path.exists(file_path):
        limit = 11
        df = pd.read_parquet(file_path, engine='fastparquet')
        print('read from parquet(hive), dataframe:\n', df[:limit])


def pandas_read_excel_demo_01():
    file_path = get_lemon_cases_excel_path()
    df = pd.read_excel(file_path, sheet_name='multiply')
    df.info()

    # 按列读取数据
    # 返回一个Series对象，title列的数据
    print('\ncol [title] as series:\n', df['title'])

    print('\ncol [title] list:', list(df['title']))
    print('col [df.title] list:', list(df.title))
    print('col [title] tuple:', tuple(df['title']))
    print('cols [index,title] dict:', dict(df['title']))  # key为数字索引

    print('\ncol [title] 1st value:', df['title'][0])

    print('\ncols [title,actual]:\n', df[['title', 'actual']])

    # 按行读取数据
    print('\nrow 1 (list):', list(df.iloc[0]))
    print('row 1 (tuple):', tuple(df.iloc[0]))
    print('row 1 (dict):', dict(df.iloc[0]))
    print('row last (dict):', dict(df.iloc[-1]))

    print('\nrow 1 [l_data]:', df.iloc[0]['l_data'])
    print('row 1 [l_data] by index:', df.iloc[0][2])

    print('\nrow 0-2:\n', df.iloc[0:3])

    # 读取所有数据
    print('\nall rows (dataframe):\n', df)
    print('\nall rows (list):\n', df.values)

    data_list = []
    for idx in df.index:
        data_list.append(df.iloc[idx].to_dict())
    print('\nall rows (list of dict):\n', data_list)


def pandas_read_excel_demo_02():
    file_path = get_lemon_cases_excel_path()
    df = pd.read_excel(file_path, sheet_name='multiply')

    # iloc, by index
    print('col 1 [index,case_id]:\n', df.iloc[:, 0])
    print('\ncol last [index,result]:\n', df.iloc[:, -1])
    print('\ncols 0-2 [index,case_id,title,l_data]:\n', df.iloc[:, 0:3])

    print('\n2-3 rows and 1-3 cols:\n', df.iloc[2:4, 1:4])
    print('\n1,3 rows and 2,4 cols:\n', df.iloc[[1, 3], [2, 4]])

    # loc, by name
    print('\n1-2 rows and col [title]:\n', df.loc[1:2, 'title'])
    print('\n1-2 rows and cols [title,l_data,r_data]:\n',
          df.loc[1:2, 'title':'r_data'])

    print('\ncols boolean(r_data > 5):\n', df['r_data'] > 5)
    print('\nrows (r_data > 5):\n', df.loc[df['r_data'] > 5])
    print('\nrows (r_data > 5) and cols [r_data,expected,actual]:\n',
          df.loc[df['r_data'] > 5, 'r_data':'actual'])


def pandas_write_excel_demo():
    file_path = get_lemon_cases_excel_path()
    df = pd.read_excel(file_path, sheet_name='multiply')

    df['result'][0] = 'test'
    output_path = os.path.join(
        os.getenv('HOME'), 'Downloads/tmp_files', 'lemon_cases_new.xlsx')
    # pip3 install openpyxl
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name='new', index=False)


def get_lemon_cases_excel_path():
    file_path = os.path.join(
        os.getenv('PYPATH'), 'pydemos', 'data', 'lemon_cases.xlsx')
    if not os.path.exists(file_path):
        raise FileNotFoundError('file not found: ' + file_path)
    return file_path


def pandas_read_csv_demo():
    file_path = os.path.join(
        os.getenv('PYPATH'), 'pydemos', 'data', 'data.log')
    if not os.path.exists(file_path):
        raise FileNotFoundError('file not found: ' + file_path)

    # csv_frame = pd.read_csv(file_path)
    # csv_frame = pd.read_csv(file_path, header=None, names=['Col1', 'Col2', 'Col3'])
    df = pd.read_csv(file_path, sep=',')
    success_df = df.loc[df['Success'] == 0]
    testtime_series = success_df['TestTime']
    print('Success TestTime Series:\n', testtime_series)

    avg_result = round(sum(testtime_series) / len(testtime_series), 2)
    print('\nmin TestTime: %r, max TestTime: %r, avg TestTime: %r'
          % (min(testtime_series), max(testtime_series), avg_result))


if __name__ == '__main__':

    # pandas_series_demo03()
    pandas_df_demo11()
    # pandas_df_pipeline()

    # pandas_plot_demo02()

    # pandas_df_save_demo()
    # pandas_df_read_demo()

    # pandas_read_excel_demo_01()
    # pandas_read_excel_demo_02()
    # pandas_write_excel_demo()
    # pandas_read_csv_demo()

    print('pandas demo DONE.')
