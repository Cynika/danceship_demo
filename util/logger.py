# -*- coding: utf-8 -*-
# zeekay
# https://stackoverflow.com/questions/7003898/

import logging
import colorlog
from functools import wraps

from util.Excption import WarnException, InfoException


class CustomFormatterStream(colorlog.ColoredFormatter):
    def format(self, record):
        if hasattr(record, 'name_override'):
            record.funcName = record.name_override
        return super(CustomFormatterStream, self).format(record)


class CustomFormatterFile(logging.Formatter):
    def format(self, record):
        if hasattr(record, 'name_override'):
            record.funcName = record.name_override
        return super(CustomFormatterFile, self).format(record)


class Logger:
    def __init__(self, logger_name, log_file):
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.ERROR)

        # 再创建一个handler，用于输出到控制台
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.INFO)

        # 规定输出格式
        formatter_fh = CustomFormatterFile(
            '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
        formatter_ch = CustomFormatterStream(
            '%(log_color)s%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

        # 定义handler的输出格式
        fh.setFormatter(formatter_fh)
        ch.setFormatter(formatter_ch)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger


def loop_exc_log(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except InfoException as ie:
                logger.info(ie, extra={'name_override': func.__name__})
            except WarnException as we:
                logger.warning(we, extra={'name_override': func.__name__})
            except SystemExit as se:
                logger.error(se, extra={'name_override': func.__name__})
                quit()
                raise se
            except Exception as e:
                logger.error(e, extra={'name_override': func.__name__})

        return wrapper

    return decorator
