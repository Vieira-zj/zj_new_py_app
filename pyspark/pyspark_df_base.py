# -*- coding: utf-8 -*-
'''
Created on 2019-04-25
@author: zhengjin

pyspark api:
http://spark.apache.org/docs/1.6.2/api/python/pyspark.sql.html

cmd for submit spark job:
bin/spark-submit \
--master yarn-client \
--driver-memory 1g \
--executor-memory 1g \
--executor-cores 2 \
--conf "spark.default.parallelism=4" \
--conf "spark.sql.shuffle.partitions=2" \
/mnt/spark_dir/pyspark_df_base.py

Note: spark shuffle asks for more memory, and in docker engine, update limited memory to 3G (2G is default)!
'''

import random
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, HiveContext
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, StringType
import pyspark.sql.functions as F


# read file on hdfs
def pyspark_df_demo01(sqlContext):
    print('read hdfs json file =>')
    # {"name":"Michael"}
    # {"name":"Andy", "age":30}
    # {"name":"Justin", "age":19}
    df_01 = sqlContext.read.format('json').load('/user/root/test/people.json')
    print('data schema: ' + str(df_01.dtypes))
    print('people count: ' + str(df_01.count()))
    print('people info:')
    df_01.show()

    # java.lang.ClassNotFoundException: Failed to find data source: com.databricks.spark.csv.
    print('read hdfs csv file =>')
    # name,age
    # Michael,37
    # Andy,30
    # Justin,19
    df_02 = sqlContext.read.format('com.databricks.spark.csv').options(
        header='true', inferschema='true').load('/user/root/test/people.csv')
    print('data schema:')
    df_02.printSchema()
    print('people count: ' + str(df_02.count()))
    print('people info:')
    df_02.show()


# init a dataframe and query
def pyspark_df_demo02(sqlContext):
    records = []
    records.append((1, 'age', '30', 50, 40))
    records.append((1, 'city', 'beijing', 50, 40))
    records.append((1, 'gender', 'fale', 50, 40))
    records.append((1, 'height', '172cm', 50, 40))
    records.append((1, 'weight', '70kg', 50, 40))

    records.append((2, 'age', '26', 100, 80))
    records.append((2, 'city', 'beijing', 100, 80))
    records.append((2, 'gender', 'fale', 100, 80))
    records.append((2, 'height', '170cm', 100, 80))
    records.append((2, 'weight', '65kg', 100, 80))

    schema = ['user_id', 'attr_name', 'attr_value', 'income', 'expenses']
    df = sqlContext.createDataFrame(records, schema)
    print('data schema:')
    df.printSchema()
    print('user count: ' + str(df.count()))
    print('users info:')
    df.show(5)

    # do shuffle for 'distinct'
    print('[distinct output] user ids:')
    df.select('user_id').distinct().show()

    print('[select output] user info with income=50:')
    df.select('user_id', 'attr_value', 'income').where('income=50').show()

    print('[orderby output] user info with income desc seq:')
    df.orderBy(df.income.desc()).show()

    print('[col add output] user info with new income:')
    df.withColumn('income_new', df.income+10).show(5)


# dataframe sql
def pyspark_df_demo03(sqlContext):
    records = []
    records.append((100, 'Katie', 19, 'brown'))
    records.append((101, 'Michael', 22, 'green'))
    records.append((102, 'Simone', 23, 'blue'))

    schema = StructType([
        StructField('id', LongType(), True),
        StructField('name', StringType(), True),
        StructField('age', LongType(), True),
        StructField('eyeColor', StringType(), True)
    ])

    df = sqlContext.createDataFrame(records, schema)
    print('data schema: ' + str(df.dtypes))
    print('swimmers count: ' + str(df.count()))

    print('swimmers:')
    df.show()

    print('[select output] get swimmers ids with age=22 by str:')
    df.select('id', 'age').filter('age=22').show()
    print('[select output] get swimmers ids with age=22 by type:')
    df.select(df.id, df.age).filter(df.age == 22).show()

    print('[select output] get swimmers ids with age=22 by str sql:')
    df.registerTempTable('swimmers')
    sqlContext.sql('select id,age from swimmers where age=22').show()

    print('[like output] get swimmers names with eye color startwith "b":')
    df.select('name', 'eyeColor').filter('eyeColor like "b%"').show()
    print('[like output] get swimmers names with eye color startwith "b" by str sql:')
    str_sql = 'select name,eyeColor from swimmers where eyeColor like "b%"'
    sqlContext.sql(str_sql).show()


# dataframe union
def pyspark_df_demo04(sqlContext):
    # same data schema for 2 dataframe
    df_01 = sqlContext.createDataFrame((
        (1, 'asf'),
        (2, '2143'),
        (3, 'rfds')
    )).toDF('label', 'sentence')
    print('df_01 data:')
    df_01.show()

    df_02 = sqlContext.createDataFrame((
        (1, 'asf'),
        (2, '2143'),
        (4, 'f8934y')
    )).toDF('label', 'sentence')
    print('df_02 data:')
    df_02.show()

    # 差集
    print('subtract output:')
    df = df_02.select('sentence').subtract(df_01.select('sentence'))
    df.show()

    # 交集
    print('intersect output:')
    df = df_02.select('sentence').intersect(df_01.select('sentence'))
    df.show()

    # 并集
    print('union output:')
    df = df_02.select('sentence').unionAll(df_01.select('sentence'))
    df.show()


# dataframe join
def pyspark_df_demo05(sc):
    from pyspark.sql import Row

    rdd = sc.parallelize(
        [Row(name='Alice', age=5, height=80), Row(name='Tom', age=10, height=70)])
    df_01 = rdd.toDF()
    print('df_01 data:')
    df_01.show()

    rdd = sc.parallelize([Row(name='Alice', weight=45), Row(name='Jim', weight=37)])
    df_02 = rdd.toDF()
    print('df_02 data:')
    df_02.show()

    # do shuffle for 'join'
    print('left join output:')
    df_01.join(df_02, df_01.name == df_02.name, 'left').show()

    # print('inner join output:')
    # df_01.join(df_02, df_01.name == df_02.name, 'inner').show()


# dataframe groupby and agg
def pyspark_df_demo06(sc, sqlContext):
    rdd = sc.parallelize(range(1, 1000), 2).map(lambda x: [random.choice('ab'), x])
    schema = StructType([
        StructField('level', StringType(), True),
        StructField('count', IntegerType(), True)])
    df = sqlContext.createDataFrame(rdd, schema).sample(False, 0.1, 999).cache()

    print('\ndataframe count: %d, and first 3 rows:' % (df.count()))
    df.show(3)

    print('\n#1: group and aggregation (max) results:')
    df1 = df.groupBy('level').agg(F.max('count').alias('count_max'))
    for item in df1.collect():
        print(item.asDict())

    print('\n#2: group and aggregation (max) results:')
    df2 = df.groupBy('level').max('count')
    print_rdd_debug_info(df2.rdd)  # partition#, 2 => 2
    df2.show()


def print_rdd_debug_info(rdd):
    print('rdd dag debug info:')
    print(rdd.toDebugString())


# dataframe distinct
def pyspark_df_demo07(hiveContext):
    course_list = [
        ('001', 'stu001', 'math'),
        ('001', 'stu002', 'math'),
        ('001', 'stu003', 'math'),
        ('002', 'stu001', 'english'),
        ('002', 'stu002', 'english'),
        ('002', 'stu003', 'english')
    ]

    schema = StructType([
        StructField('course_id', StringType(), False),
        StructField('user_id', StringType(), False),
        StructField('course_name', StringType(), False)
    ])

    df = hiveContext.createDataFrame(course_list, schema).coalesce(1).cache()

    # 整行去重
    print('\n#1: distinct course_id+course_name:')
    df.select('course_id', 'course_name').distinct().show()

    # 某一列或者多列相同的去除重复
    print('\n#2: distince col course_id and course_name:')
    df2 = df.distinct().dropDuplicates(
        subset=[c for c in df.columns if c in ['course_id', 'course_name']])
    df2.select('user_id', 'course_id', 'course_name').show()


# dataframe hive table
def pyspark_df_demo08(hiveContext):
    course_list = [
        ('001', 'math'),
        ('002', 'chinese'),
        ('003', 'english'),
        ('004', 'computer')
    ]

    schema = StructType([
        StructField('course_id', StringType(), False),
        StructField('course_name', StringType(), False)
    ])

    df = hiveContext.createDataFrame(course_list, schema).coalesce(1).cache()
    df.show()

    save_table = 'course_table1'
    print('\n#1: save df as hive table (%s) by saveAsTable().' % save_table)
    df.write.format('orc').mode('overwrite').saveAsTable(save_table)

    save_table = 'course_table2'
    print('\n#2: save df as hive table (%s) by sql "insert overwrite".' % save_table)
    hiveContext.sql("CREATE TABLE IF NOT EXISTS %s ( \
        course_id string COMMENT '课程ID', \
        course_name string COMMENT '')COMMENT '课程名称'" % save_table)

    df.registerTempTable('tmp_table_df')
    hiveContext.sql('insert overwrite table %s select * from tmp_table_df' % save_table)

    # output:
    # hdfs dfs -ls -R /user/hive/warehouse
    # /user/hive/warehouse/course_table1/part-r-00000-8f23206b-cb18-418c-82d9-ff493b978960.orc
    # /user/hive/warehouse/course_table2/part-00000


# dataframe 拆分多项
def pyspark_df_demo09(hiveContext):
    course_list = [
        ('001', 'math', 'stu001,stu002,stu003'),
        ('002', 'english', 'stu001,stu003,stu004'),
    ]

    schema = StructType([
        StructField('course_id', StringType(), nullable=False),
        StructField('course_name', StringType(), nullable=False),
        StructField('student_ids', StringType(), nullable=False)
    ])

    df = hiveContext.createDataFrame(course_list, schema).coalesce(1).cache()
    df.show()

    print('\none row split to multiple rows.')
    df.withColumn('student_id', F.explode(F.split(df['student_ids'], ','))) \
        .drop(df['student_ids']).show()


# dataframe 多项合并
def pyspark_df_demo10(hiveContext):
    course_list = [
        ('001', 'math', 'desc001', 'desc002', 'desc003'),
        ('002', 'english', 'desc011', 'desc012', 'desc013')
    ]

    schema = StructType([
        StructField('course_id', StringType(), nullable=False),
        StructField('course_name', StringType(), nullable=False),
        StructField('comment_1', StringType(), nullable=False),
        StructField('comment_2', StringType(), nullable=False),
        StructField('comment_3', StringType(), nullable=False)
    ])

    df = hiveContext.createDataFrame(course_list, schema).coalesce(1).cache()
    df.show()

    print('\nmultiple fields merge into one field.')
    df.withColumn('all_comments', F.concat_ws(
        '|', df['comment_1'], df['comment_2'], df['comment_3'])).show()


if __name__ == '__main__':

    conf = SparkConf().setAppName('pyspark_df_base_test').setMaster('yarn-client')
    sc = SparkContext(conf=conf)
    print('pyspark version: ' + str(sc.version))
    sqlContext = SQLContext(sc)
    hiveContext = HiveContext(sc)

    # pyspark_df_demo04(sqlContext)
    # pyspark_df_demo05(sc)
    # pyspark_df_demo06(sc, sqlContext)
    pyspark_df_demo10(hiveContext)

    print('pyspark dataframe base demo DONE.')
