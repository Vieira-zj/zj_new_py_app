# coding=utf-8

import copy
import inspect
import logging
import time
import traceback
import uuid
from abc import abstractmethod
from queue import Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Event(object):

    def __init__(self, event_id, message, channel):
        self._id = event_id
        self._msg = message
        self._channel = channel

    @property
    def id(self):
        return self._id

    @property
    def message(self):
        return self._msg

    @property
    def channel(self):
        return self._channel

    def __str__(self):
        return f'[event: id={self._id}, message={self._msg}, channel={self._channel}]'


class BaseServer(object):

    def __init__(self):
        self._running = False
        self._thread = None

    @property
    def thread(self):
        return self._thread

    def start(self, *args, **kwargs):
        if self._running:
            return

        logger.info('server is started.')
        self._running = True
        self._thread = Thread(target=self.run, args=args, kwargs=kwargs)
        self._thread.start()

    @abstractmethod
    def run(self):
        """ run server. """

    def stop(self):
        self._running = False
        logger.info('server is stopped.')


class EventBusServer(BaseServer):

    def __init__(self):
        super().__init__()
        self._events_queue = Queue(maxsize=10)
        self._channel_subs = {}
        self._executor = ThreadPoolExecutor(
            max_workers=3, thread_name_prefix='eventbus-')

    def run(self):
        while self._running:
            try:
                e = self._events_queue.get(block=True)  # block for a event
                e = copy.deepcopy(e)
                logger.info('get a event: ' + str(e))
                callback_fn_list = self._channel_subs.get(e.channel, [])
                for cb_fn, args, kwargs in callback_fn_list:
                    self._executor.submit(
                        self._callback_fn_handler, cb_fn, e, args, kwargs)
            except Exception:
                traceback.print_exc()

    def _callback_fn_handler(self, callback_fn, event, args, kwargs):
        fn_sig = inspect.signature(callback_fn)
        fn_params = list(fn_sig.parameters.values())
        if len(fn_params) < 1:
            logger.error(
                f'Event callback function [{callback_fn.__name__}] need a argument for receiving event object.')
            return

        callback_args = []
        callback_args.append(event.message)
        callback_args.extend(args)

        logger.info(
            f'invoke callback function: {callback_fn.__name__}, arguments: {callback_args}')
        try:
            callback_fn(*callback_args, **kwargs)
        except Exception:
            logger.error('Event callback function [%s] error:\n%s' % (
                callback_fn.__name__, traceback.format_exc()))

    def stop(self):
        super().stop()
        self.publish('system', 'stop')

    def publish(self, channel, message):
        event_id = uuid.uuid4()
        event = Event(event_id, message, channel)
        self._events_queue.put(event, block=True)

    def subscribe(self, channel, callback_fn, *args, **kwargs):
        callback_fn_list = self._channel_subs.setdefault(channel, [])
        callback_fn_list.append((callback_fn, args, kwargs))

    def unsubscribe(self, channel, callback_fn, *args, **kwargs):
        callback_fn_list = self._channel_subs.get(channel, [])
        for item in callback_fn_list:
            if item[0].__name__ == callback_fn.__name__:
                callback_fn_list.remove(item)
                return


def test_eventbus_server():
    def callback_cal(message, a, b):
        ret = 0
        if message == 'add':
            ret = a + b
        elif message == 'min':
            ret = a - b
        time.sleep(0.5)
        logger.info('results: ' + str(ret))

    def callback_msg(message):
        time.sleep(0.5)
        logger.info('event message: ' + message)

    # create server
    channel = 'calculate'
    server = EventBusServer()
    server.subscribe(channel, callback_cal, 3, 1)
    server.subscribe(channel, callback_msg)
    server.start()

    # send events
    try:
        for msg in ('add', 'min', 'add'):
            server.publish(channel, msg)
        time.sleep(3)

        logger.info('unsubscribe a callback: ' + callback_cal.__name__)
        server.unsubscribe(channel, callback_cal)
        for msg in ('add', 'min'):
            server.publish(channel, msg)
        time.sleep(3)
    finally:
        if server:
            server.stop()
    server.thread.join()


if __name__ == '__main__':

    test_eventbus_server()
    logger.info('main exit.')
