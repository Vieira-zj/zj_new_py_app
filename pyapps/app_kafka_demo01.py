# -*- coding: utf-8 -*-
'''
Created on 2019-01-08
@author: zhengjin

Pre condition:
1. pip3 install kafka-python 
2. in /etc/hosts, add: 127.0.0.1 zjmbp

Reference:
https://kafka-python.readthedocs.io/en/latest/usage.html
'''

import json
import random
import multiprocessing
import os
import time

from kafka import KafkaConsumer
from kafka import KafkaProducer


def process_producer(topic, server):
    def _on_send_sucess(record_metadata):
        print('send message success [event]:')
        print('\tmeta topic:', record_metadata.topic)
        print('\tmeta partition:', record_metadata.partition)
        print("\toffset:", record_metadata.offset)

    def _on_send_failed(excp):
        print('send message failed [event]:', excp)

    print('\npid=%d, producer send msgs ...' % os.getpid())
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers=[server], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
        for i in range(10):
            msg_dict = {
                'index': str(i + random.randint(1, 100)),
                'stat': 'ok',
            }
            future = producer.send(topic, value=msg_dict)
            future.add_callback(_on_send_sucess).add_errback(_on_send_failed)
            time.sleep(0.2)
    finally:
        if producer is not None:
            producer.flush()
            producer.close()
            print('producer session closed.')


def process_consumer(topic, server):
    print('\npid=%d, consumer receive msg ...' % os.getpid())
    consumer = None
    try:
        consumer = KafkaConsumer(
            topic, bootstrap_servers=[server],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for msg in consumer:
            recv_msg = 'received msg => %s:%d:%d: key=%s value=%s' % (
                msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            print(recv_msg)
    finally:
        if consumer is not None:
            consumer.close()
            print('consumer session closed.')


if __name__ == '__main__':

    topic = 'test_topic'
    server = 'zjmbp:9094'

    # consumer
    c = multiprocessing.Process(target=process_consumer, args=(topic, server))
    c.start()
    time.sleep(2)

    # producer1
    p1 = multiprocessing.Process(target=process_producer, args=(topic, server))
    p1.start()
    p1.join(timeout=5)
    if p1.is_alive():
        p1.kill()
    time.sleep(2)

    # producer2
    p2 = multiprocessing.Process(target=process_producer, args=(topic, server))
    p2.start()
    p2.join(timeout=5)
    if p1.is_alive():
        p1.kill()

    c.join(timeout=5)
    if c.is_alive():
        print('kill consumer process(pid=%d)!' % c.pid)
        c.kill()

    print('kafka test demo DONE.')
