# -*- coding: utf-8 -*-
'''
Created on 2019-08-13
@author: zhengjin

Conditions:
$ hdfs dfs -mkdir -p /user/root/test

Submit spark job:
bin/spark-submit \
--master yarn-client \
--driver-memory 1g \
--num-executors 1 \
--executor-memory 1g \
--executor-cores 2 \
/mnt/spark_dir/data_prepare02.py
'''

import datetime
import random

import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext


def print_df_info(df):
    print('\nDATAFRAME INFO:')
    print('data schema:')
    df.printSchema()
    print('records count: %d' % df.count())
    print('top 10 records:')
    df.show(10)


def print_rdd_debug_info(rdd):
    print('\nRDD DEBUG INFO:')
    print('rdd number of partitions: ' + str(rdd.getNumPartitions()))
    print('rdd dag details:')
    print(rdd.toDebugString())


class DataCreate(object):

    def __init__(self, sc, sqlContext, hiveContext):
        self._sc = sc
        self._sqlContext = sqlContext
        self._hiveContext = hiveContext

    def data_prepare(self, write_path, row_count, dt, dt_n, part_n=1, f_type='parquet'):
        '''
        Create parquet or orc files partitioned by dt (date).
        '''
        schema = ['id', 'flag']
        write_path = self._format_path(write_path)
        dt_timestamp = datetime.datetime.strptime(dt, '%Y%m%d')

        start = 0
        for i in range(dt_n):
            test_rdd = self._sc.parallelize(range(start, start+row_count), part_n) \
                .map(lambda x: [x, str(x) + random.choice('yn')])
            test_df = self._hiveContext.createDataFrame(test_rdd, schema)

            dt = datetime.datetime.strftime(
                dt_timestamp + datetime.timedelta(days=i), '%Y%m%d')
            if f_type == 'orc':
                test_df.write.orc(write_path + dt)
            else:
                test_df.write.parquet(write_path + dt)

            start += row_count

    def _format_path(self, path):
        if path.endswith('/'):
            path += 'dt='
        else:
            path += '/dt='
        return path
# DataCreate class end


class DataLoad(object):

    def __init__(self, sc, sqlContext, hiveContext):
        self._sc = sc
        self._sqlContext = sqlContext
        self._hiveContext = hiveContext

    def _pre_load(self, d_path, s_date, e_date):
        d_path = self._format_path(d_path)

        f_paths = []
        s_date_timestamp = datetime.datetime.strptime(s_date, '%Y%m%d')
        e_date_timestamp = datetime.datetime.strptime(e_date, '%Y%m%d')
        while s_date_timestamp <= e_date_timestamp:
            f_paths.append(
                d_path + datetime.datetime.strftime(s_date_timestamp, '%Y%m%d'))
            s_date_timestamp += datetime.timedelta(days=1)

        return f_paths

    def _format_path(self, path):
        if path.endswith('/'):
            path += 'dt='
        else:
            path += '/dt='
        return path

    def load_data_parquet(self, d_path, s_date, e_date):
        '''
        Load data from parquet files by dt (start_date, end_date).
        '''
        f_paths = self._pre_load(d_path, s_date, e_date)
        return self._sqlContext.read.parquet(*f_paths)

    def load_data_orc(self, d_path, s_date, e_date):
        '''
        Load data from orc files by dt (start_date, end_date).
        '''
        read_dfs = []
        f_paths = self._pre_load(d_path, s_date, e_date)
        for f_path in f_paths:
            try:
                df = self._hiveContext.read.orc(f_path)
            except Exception as e:
                print(e)
                continue
            read_dfs.append(df)

        ret_df = read_dfs[0]
        for _ in range(1, len(read_dfs)):
            ret_df = ret_df.unionAll(df)
        return ret_df
# DataLoad class end


def testDataPrepareForParquet(sc, sqlContext, hiveContext):
    d_path = 'hdfs:///user/root/test/test_parquet/'
    start_date = '20190701'

    dataCreate = DataCreate(sc, sqlContext, hiveContext)
    dataCreate.data_prepare(d_path, 11000, start_date, 3, f_type='parquet')

    load = DataLoad(sc, sqlContext, hiveContext)
    df = load.load_data_parquet(d_path, start_date, '20190703')
    print_df_info(df)
    # output:
    # /user/root/test/test_parquet/dt=20190701
    # /user/root/test/test_parquet/dt=20190702
    # /user/root/test/test_parquet/dt=20190703


def testDataPrepareForOrc(sc, sqlContext, hiveContext):
    d_path = 'hdfs:///user/root/test/test_orc/'
    start_date = '20190701'

    dataCreate = DataCreate(sc, sqlContext, hiveContext)
    dataCreate.data_prepare(d_path, 12000, start_date, 3, f_type='orc')

    load = DataLoad(sc, sqlContext, hiveContext)
    df = load.load_data_orc(d_path, start_date, '20190703')
    print_df_info(df)
    # output:
    # /user/root/test/test_orc/dt=20190701
    # /user/root/test/test_orc/dt=20190702
    # /user/root/test/test_orc/dt=20190703


def testUpdateDFColumns(sc, sqlContext, hiveContext):
    from pyspark.sql.types import StringType, IntegerType
    import pyspark.sql.functions as F

    d_path = 'hdfs:///user/root/test/test_parquet/'
    start_date = '20191001'

    dataCreate = DataCreate(sc, sqlContext, hiveContext)
    dataCreate.data_prepare(d_path, 12000, start_date, 3, f_type='parquet')

    load = DataLoad(sc, sqlContext, hiveContext)
    df = load.load_data_parquet(d_path, start_date, '20191003')
    print('###src rdd number of partitions: ' + str(df.rdd.getNumPartitions()))

    # repartition with shuffle
    df = df.repartition(4).cache()
    print_df_info(df)
    print_rdd_debug_info(df.rdd)

    print('##1: update dataframe with new column "isOK":')
    # df1 = df.withColumn('isOK', F.col('flag'))
    df1 = df.withColumn('isOK', df['flag'])
    print_df_info(df1)

    print('##2: update dataframe column type, id:long => id:int:')
    # df2 = df.withColumn('id', F.col('id').cast(IntegerType()))
    df2 = df.withColumn('id', df['id'].cast(IntegerType()))
    print_df_info(df2)

    print('##3: dataframe column format with select.')
    print('id:long => id_str:string, flag:string => is_ok:string:')
    df3 = df.select(
        df['id'].cast(StringType()).alias('id_str'),
        df['flag'].alias('is_ok')
    )
    print_df_info(df3)

    print('###dataframe write to parquet (4 partitions).')
    w_path = 'hdfs:///user/root/test/write_parquet/'
    df.write.parquet(w_path, mode='overwrite')
    # write files:
    # /user/root/test/write_parquet/part-r-00000-15f7284b-1263-4129-9389-bf1effcf198c.gz.parquet
    # /user/root/test/write_parquet/part-r-00001-15f7284b-1263-4129-9389-bf1effcf198c.gz.parquet
    # /user/root/test/write_parquet/part-r-00002-15f7284b-1263-4129-9389-bf1effcf198c.gz.parquet
    # /user/root/test/write_parquet/part-r-00003-15f7284b-1263-4129-9389-bf1effcf198c.gz.parquet


if __name__ == '__main__':

    conf = SparkConf().setAppName('data_prepare_demo').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)
    hiveContext = HiveContext(sc)

    # testDataPrepareForParquet(sc, sqlContext, hiveContext)
    # testDataPrepareForOrc(sc, sqlContext, hiveContext)
    testUpdateDFColumns(sc, sqlContext, hiveContext)

    print('pyspark data prepare demo DONE.')
