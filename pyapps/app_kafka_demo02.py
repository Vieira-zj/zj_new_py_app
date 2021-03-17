# -*- coding: utf-8 -*-
'''
Created on 2019-01-08
@author: zhengjin

Pre condition: 
1. pip3 install kafka-python 
2. in /etc/hosts, add: 127.0.0.1 zjmbp
'''

import json
import random
import sys
import multiprocessing
import time

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
from kafka.errors import KafkaError, KafkaTimeoutError


class Producer(object):

    def __init__(self, server_list, client_id, topic):
        '''
        KafkaProducer构造函数参数解释:
        - acks 0表示发送不理睬发送是否成功; 1表示需要等待leader成功写入日志才返回; all表示所有副本都写入日志才返回.
        - buffer_memory 默认33554432也就是32M, 该参数用于设置producer用于缓存消息的缓冲区大小. 如果采用异步发送消息, 
            那么生产者启动后会创建一个内存缓冲区用于存放待发送的消息, 然后由专属线程来把放在缓冲区的消息进行真正发送. 
            如果要给生产者要给很多分区发消息那么就需要考虑这个参数的大小, 防止过小降低吞吐量.
        - compression_type 是否启用压缩, 默认是none, 可选类型为gzip, lz4, snappy三种.
            压缩会降低网络IO但是会增加生产者端的CPU消耗.
            另外如果broker端的压缩设置和生产者不同, 那么也会给broker带来重新解压缩和重新压缩的CPU负担.
        - retries 重试次数, 当消息发送失败后会尝试几次重发. 
            默认为0, 一般考虑到网络抖动或者分区的leader切换, 而不是服务端真的故障所以可以设置重试3次.
        - retry_backoff_ms 每次重试间隔多少毫秒, 默认100毫秒.
        - batch_size 对于调优生产者吞吐量和延迟性能指标有重要的作用. 
            buffer_memeory可以看做池子, 而这个batch_size可以看做池子里装有消息的小盒子. 
            这个值默认16384也就是16K, 其实不大. 生产者会把发往同一个分区的消息放在一个batch中, 
            当batch满了就会发送里面的消息, 但是也不一定非要等到满了才会发. 
            这个数值大那么生产者吞吐量高, 但是性能低, 因为盒子太大占用内存发送的时候这个数据量也就大. 
            如果你设置成1M, 那么显然生产者的吞吐量要比16K高的多.
        - linger_ms 上面说batch没有填满也可以发送, 那显然有一个时间控制, 就是这个参数, 默认是0毫秒. 
            这个参数就是用于控制消息发送延迟多久的. 默认是立即发送, 无需关系batch是否填满. 
            大多数场景我们希望立即发送, 但是这也降低了吞吐量.
        - request_timeout_ms 生产者发送消息后, broker需要在规定时间内将处理结果返回给生产者, 
            那个这个时间长度就是这个参数控制的, 默认30000, 也就是30秒. 
            如果broker在30秒内没有给生产者响应, 那么生产者就会认为请求超时, 并在回调函数中进行特殊处理, 或者进行重试.
        '''
        self._kwargs = {
            'bootstrap_servers': server_list,
            'client_id': client_id,
            'acks': 1,
            'buffer_memory': 33554432,
            'compression_type': None,
            'retries': 3,
            'batch_size': 1048576,
            'key_serializer': lambda m: json.dumps(m).encode('utf-8'),
            'value_serializer': lambda m: json.dumps(m).encode('utf-8'),
        }
        self._producer = KafkaProducer(**self._kwargs)
        self._topic = topic

    def close_connection(self, timeout=3):
        if self._producer is not None:
            # 关闭生产者, 可以指定超时时间, 也就是等待关闭成功最多等待多久
            self._producer.close(timeout=timeout)

    def send_msg(self, value):
        '''
        - value 必须必须为字节或者被序列化为字节, 由于之前我们初始化时已经通过value_serializer来做了, 所以我上面的语句就注释了
        - key 与value对应的键, 可选, 也就是把一个键关联到这个消息上. 
            key相同就会把消息发送到同一分区上, 所以如果有这个要求就可以设置key, 也需要序列化.
        - partition 发送到哪个分区, 整型. 如果不指定将会自动分配.
        '''
        kwargs = {
            'value': value,
            'key': None,
            'partition': None
        }

        # 发送的消息必须是序列化后的，或者是字节.
        # message = json.dumps(msg, encoding='utf-8', ensure_ascii=False)
        try:
            # 异步发送, 发送到缓冲区, 同时注册两个回调函数, 一个是发送成功的回调, 一个是发送失败的回调
            future = self._producer.send(self._topic, **kwargs)
            future.add_callback(self._on_send_sucess).add_errback(self._on_send_failed)
        except KafkaTimeoutError as e:
            print(e)

    def send_msg_now(self, timeout=3):
        '''
        调用flush()函数可以放所有在缓冲区的消息记录立即发送, 即使ligner_ms值大于0.
        这时候后台发送消息线程就会立即发送消息并且阻塞, 等待消息发送成功, 当然阻塞还取决于acks的值.
        如果不调用flush函数, 那么什么时候发送消息取决于ligner_ms或者batch任意一个条件满足就会发送.
        '''
        try:
            self._producer.flush(timeout=timeout)
        except KafkaTimeoutError as e:
            print(e)

    def _on_send_sucess(self, record_metadata):
        '''
        异步发送成功回调函数, 也就是真正发送到kafka集群且成功才会执行. 发送到缓冲区不会执行回调方法.
        '''
        print('message send success [event]:')
        print('\tsend topic:', record_metadata.topic)
        print('\tsend partition:', record_metadata.partition)
        # 这个偏移量是相对偏移量, 也就是相对起止位置, 也就是队列偏移量
        print('\toffset:', record_metadata.offset)

    def _on_send_failed(self, excp):
        print('message send failed [event]:', excp)


class Consumer(object):

    def __init__(self, server_list, group_id, client_id, topic):
        self._server_list = server_list
        self._group_id = group_id
        self._topic = topic
        self._client_id = client_id

    def consume_msg(self):
        '''
        初始化一个消费者实例. 消费者不是线程安全的, 所以建议一个线程实现一个消费者, 而不是一个消费者让多个线程共享.
        下面这些是可选参数, 可以在初始化KafkaConsumer实例的时候传递进去.
        - enable_auto_commit 是否自动提交, 默认是true.
        - auto_commit_interval_ms 自动提交间隔毫秒数.
        - auto_offset_reset='earliest' 重置偏移量, earliest移到最早的可用消息, latest最新的消息, 默认为latest.
        '''
        consumer = KafkaConsumer(
            self._topic, bootstrap_servers=self._server_list,
            group_id=self._group_id, client_id=self._client_id,
            enable_auto_commit=True, auto_commit_interval_ms=5000, auto_offset_reset='latest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        '''
        这里不需要显示的调用订阅函数, 在初始化KafkaConsumer对象的时候已经指定了主题, 
        如果主题字段不为空则会自动调用订阅函数, 至于这个线程消费哪个分区则是自动分配的. 
        如果你希望手动指定分区则就需要使用 assign() 函数, 并且在初始的时候不输入主题.
        '''
        # consumer.subscribe(self._topic_list)
        # consumer.assign([TopicPartition(topic='Test', partition=0), TopicPartition(topic='Test', partition=1)])
        print('subscribe topic:', consumer.subscription())
        print('consume partition:', consumer.partitions_for_topic(self._topic))

        try:
            for msg in consumer:
                if msg:
                    print('received msg => Topic: %s Partition: %d Offset: %s Key: %s Message: %s'
                          % (msg.topic, msg.partition, msg.offset, msg.key, msg.value))
        finally:
            if consumer is not None:
                consumer.close()


def process_producer(server_list, client_id, topic):
    print('send message ...')
    producer = Producer(server_list, client_id, topic)
    try:
        begin = random.randint(0, 100)
        for i in range(10):
            msg = {
                'publisher': 'procucer_test',
                'ticket_code': 60000 + begin + i,
                'cur_price': random.randint(1, 500),
            }
            producer.send_msg(value=msg)
            time.sleep(0.2)
    finally:
        if producer is not None:
            producer.send_msg_now()
            producer.close_connection()


def process_consumer(server_list, group_id, client_id, topic):
    print('receive message ...')
    consumer = Consumer(server_list, group_id, client_id, topic)
    consumer.consume_msg()


if __name__ == '__main__':

    kafka_server = ['zjmbp:9094']
    group_id = 'kafka_test_consumer_group'
    client_id = 'kafka_test_client'
    topic = 'zjtest_topic'

    # producer1
    p1 = multiprocessing.Process(target=process_producer, args=(kafka_server, client_id, topic))
    p1.start()
    p1.join(timeout=5)
    if p1.is_alive():
        p1.kill()
    time.sleep(1)

    # consumer
    c = multiprocessing.Process(target=process_consumer, args=(kafka_server, group_id, client_id, topic))
    c.start()
    time.sleep(2)

    # producer2
    p2 = multiprocessing.Process(target=process_producer, args=(kafka_server, client_id, topic))
    p2.start()
    p2.join(timeout=5)
    if p2.is_alive():
        p2.kill()
    time.sleep(1)

    c.join(timeout=5)
    if c.is_alive():
        print('kill consumer process(pid=%d)!' % c.pid)
        c.kill()

    print('kafka test demo DONE.')
