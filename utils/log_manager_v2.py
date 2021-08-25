# coding=utf-8

import os
import logging

from collections import namedtuple
from colorama import Fore, Style, Back
from pathlib import Path

logger_key = 'logger manager'
is_logger_init = False


def get_logger() -> logging.Logger:
    global is_logger_init
    if not is_logger_init:
        __init_stream_logger()
        is_logger_init = True
    return logging.getLogger(logger_key)


def __init_stream_logger():
    color_format = ColorFormater()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(color_format)

    logger: logging.Logger = logging.getLogger(logger_key)
    logger.addHandler(stream_handler)


def _init_file_logger(log_file_path):
    path = Path(log_file_path)
    if not path.exists():
        raise FileNotFoundError(log_file_path)

    log_file = path.expanduser().resolve()
    file_formater = logging.Formatter(
        fmt='%(asctime)s %(levelname)s [%(module)s] - %(threadName)s [PID] %(process)s - %(message)s'
    )
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, backupCount=1, encoding='utf-8')
    file_handler.setFormatter(file_formater)

    logger: logging.Logger = logging.getLogger(logger_key)
    logger.addHandler(file_handler)


#
# color
#

color = namedtuple('Color', ['fore', 'style', 'back'])

colors = {
    'notice': color(fore=Fore.GREEN, style=Style.NORMAL, back=Back.RESET),
    'critical': color(fore=Fore.WHITE, style=Style.BRIGHT, back=Back.RED),
    'error': color(fore=Fore.RED, style=Style.NORMAL, back=Back.RESET),
    'warning': color(fore=Fore.YELLOW, style=Style.NORMAL, back=Back.RESET),
    'info': color(fore=Fore.WHITE, style=Style.NORMAL, back=Back.RESET),
    'debug': color(fore=Fore.GREEN, style=Style.NORMAL, back=Back.RESET),
}


def colorit(level: str, text: str) -> str:
    level = level.lower()
    c = colors.get(level, '')
    if c:
        return f'{c.fore}{c.style}{c.back}{text}{Style.RESET_ALL}'
    return text


class ColorFormater(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        levelname = f'{colorit(level, record.levelname)}'
        module = f'{colorit(level, record.module)}'
        msg = f'{colorit(level, record.msg)}'
        return f'{levelname} [{module}]: {msg}'

#
# main
#


if __name__ == '__main__':

    logger = get_logger()
    logger.setLevel(logging.DEBUG)

    logger.debug('log manager debug test.')
    logger.info('log manager info test.')
    logger.warning('log manager warning test.')
    logger.error('log manager error test.')
    logger.critical('log manager critical test.')
