# -*- coding: utf-8 -*-
'''
Created on 2019-05-22
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
/mnt/spark_dir/data_prepare01.py
'''

import random
import numpy as np
import uuid

import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext


TYPE_LIST = 'abcdefghijklmnopqrstuvwxyz'
FLAG_LIST = map(str, range(2))
# FLAG_LIST = (str(i) for i in range(2))


def gen_evt_id(prefix):
    return prefix + '_' + str(uuid.uuid4())


def print_df_info(pyspark_df):
    print('\nDATAFRAME INFO:')
    print('data schema:')
    pyspark_df.printSchema()
    print('records count: ' + str(pyspark_df.count()))
    print('top 5 records:')
    pyspark_df.show(5)


# demo01: generate parquet data
def pyspark_data_demo01(sc, sqlContext):
    print('generate test data (parquet).')
    test_rdd = sc.parallelize(range(1000), 1) \
        .map(lambda x: [x, str(x) + '_' + random.choice('yn')])
    test_df = sqlContext.createDataFrame(test_rdd, ['id', 'flag'])
    print_df_info(test_df)

    write_dir = 'hdfs:///user/root/test/testdata'
    test_df.write.parquet(write_dir)
    print('write test data as parquet success.')

    # hdfs dfs -ls -h /user/root/test/testdata
    # outputs:
    # /user/root/test/testdata/_SUCCESS
    # /user/root/test/testdata/part-r-00000-408a9e55-ce05-4aeb-aecb-c0de0f5e10cb.gz.parquet


# demo02: generate parquet data
def extend_tbl_account(id_account_rdd):

    def _extend_acount(account_id):
        account_type = 'acc_' + random.choice(TYPE_LIST)
        offshore = random.choice(FLAG_LIST)
        open_date = '2017-0%d-%d' % (random.randint(1, 9), random.randint(10, 30))
        close_date = '2019-0%d-%d' % (random.randint(1, 9), random.randint(10, 30))
        return [account_id, account_type, offshore, open_date, close_date]

    result_rdd = id_account_rdd.map(lambda x: _extend_acount(x))
    schema = ['account_id', 'account_type', 'offshore', 'open_date', 'close_date']
    return result_rdd, schema


def pyspark_data_demo02(sc, sqlContext):
    print('generate id_account_list.')
    num_account = 1500
    id_account_rdd = sc.parallelize(range(num_account), 1) \
        .map(lambda x: gen_evt_id('acc'))
    id_account_rdd.persist(storageLevel=pyspark.StorageLevel.MEMORY_AND_DISK)

    print('extend tbl_account by account_ids:')
    tbl_account_rdd, schema_account = extend_tbl_account(id_account_rdd)
    tbl_account_df = sqlContext.createDataFrame(tbl_account_rdd, schema_account)
    print_df_info(tbl_account_df)

    write_dir = 'hdfs:///user/root/test/account'
    tbl_account_df.write.parquet(write_dir)
    id_account_rdd.unpersist()
    print('write id_account_list success.')

    # hdfs dfs -ls -h /user/root/test/account
    # outputs:
    # /user/root/test/account/_SUCCESS
    # /user/root/test/account/part-r-00000-7523b316-5d48-46db-8bf4-8c74ce1ef3ec.gz.parquet


# demo03: read and rewrite parquet
def pyspark_data_demo03(sc, sqlContext):
    import pyspark.sql.functions as F
    import pyspark.sql.types as T

    def extend_index(col1, col2):
        return str(col2) + '_' + col1
    udf_extend_index = F.udf(extend_index, T.StringType())

    # read data from parquet
    read_dir = 'hdfs:///user/root/test/account/'
    parquet_file = 'part-r-00000-ef28bf7f-19b0-4430-9bd4-39a67ed1c390.gz.parquet'
    print('read id_account_list parquet file: ' + read_dir + parquet_file)
    id_account_df = sqlContext.read.parquet(read_dir + parquet_file)
    id_account_df.persist(storageLevel=pyspark.StorageLevel.MEMORY_AND_DISK)
    print('read id_account_list success.')
    print_df_info(id_account_df)

    # copy df with new account_ids, and write to parquet
    write_dir = 'hdfs:///user/root/test/new_account/'
    for i in range(2, 4):
        new_id_account_df = id_account_df.withColumn('tmp_index', F.lit(i)) \
            .withColumn('new_id', udf_extend_index('account_id', 'tmp_index')) \
            .drop('tmp_index') \
            .drop('account_id') \
            .withColumnRenamed('new_id', 'account_id')
        print('create new id_account_list #' + str(i))
        print_df_info(new_id_account_df)

        new_id_account_df.write.mode('overwrite') \
            .parquet(write_dir + 'account_' + str(i))
        print('write new id_account_list success.')

    id_account_df.unpersist()

    # outputs:
    # /user/root/test/new_account/account_2/_SUCCESS
    # /user/root/test/new_account/account_2/part-r-00000-d3427ae9-dbb9-49a6-9228-f68ca8e1ef38.gz.parquet
    # /user/root/test/new_account/account_3/_SUCCESS
    # /user/root/test/new_account/account_3/part-r-00000-57715fe2-9f00-486f-863d-2c3a9fa510e7.gz.parquet


# demo04: prepare bank data
def pyspark_data_demo04(sc, sqlContext):
    jobs = ['technician', 'management', 'blue-collar', 'entrepreneur',
            'services', 'admin', 'housemaid', 'unemployed', 'unknown', 'retired']
    maritals = ['married', 'divorced', 'single']
    educations = ['unknown', 'university.degree', 'professional.course',
                  'high.school', 'basic.4y', 'basic.6y', 'basic.9y']
    flag = ['yes', 'no']
    contacts = ['cellular', 'telephone']
    months = ['jun', 'feb', 'mar', 'apr', 'may', 'jun',
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri']
    poutcomes = ['nonexistent', 'success', 'failure']
    labels = [0, 1]
    dates = ['2015-3-20', '2015-4-20', '2015-4-21']

    def _extend_bank_record(record_id):
        fields = [record_id]  # id
        fields.append(random.randint(18, 85))  # age
        fields.append(random.choice(jobs))  # job
        fields.append(random.choice(maritals))  # marital
        fields.append(random.choice(educations))  # education
        fields.append(random.choice(flag))  # default
        fields.append(random.choice(flag))  # housing
        fields.append(random.choice(flag))  # load
        fields.append(random.choice(contacts))  # contact
        fields.append(random.choice(months))  # month
        fields.append(random.choice(days_of_week))  # day_of_week
        fields.append(random.randint(1, 199))  # duration
        fields.append(random.randint(1, 199))  # campaign
        fields.append(random.choice([3, 6, 999]))  # pdays
        fields.append(random.choice([0, 1]))  # previous
        fields.append(random.choice(poutcomes))  # poutcome
        fields.append(float('%.2f' % np.random.uniform(-3., 2.)))  # emp_var_rate
        fields.append(float('%.3f' % np.random.uniform(92., 94.)))  # cons_price_idx
        fields.append(random.choice(labels))  # y
        fields.append(random.choice(dates))  # date1
        fields.append('2015-4-20')  # date2
        fields.append('2015-4-20')  # date3

        return fields

    print('generate bank_data start.')
    num_bankdata = 2 * 10000
    num_partitions = 1
    bankdata_rdd = sc.parallelize(range(num_bankdata), num_partitions) \
        .map(lambda x: gen_evt_id('acc')) \
        .map(lambda id: _extend_bank_record(id))
    # bankdata_rdd.repartition(1)

    schema = ['id', 'age', 'job', 'marital', 'education', 'default',
              'housing', 'loan', 'contact', 'month', 'day_of_week', 'duration',
              'campaign', 'pdays', 'previous', 'poutcome', 'emp_var_rate',
              'cons_price_idx', 'y', 'date1', 'date2', 'date3']
    bankdata_df = sqlContext.createDataFrame(bankdata_rdd, schema)
    print_df_info(bankdata_df)

    write_dir = 'hdfs:///user/root/test/bankdata'
    bankdata_df.write.parquet(write_dir)
    print('write band_data success.')


if __name__ == '__main__':

    conf = SparkConf().setAppName('data_prepare_demo').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)

    pyspark_data_demo04(sc, sqlContext)
    print('pyspark data prepare demo DONE.')
