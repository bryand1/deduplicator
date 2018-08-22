import logging
from sys import stdout
from time import gmtime
from typing import Iterable

from app import config


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    logger.propagate = False
    formatter = logging.Formatter(config.LOG_MSG_FORMAT, datefmt=config.LOG_DATE_FORMAT)
    formatter.converter = gmtime
    handler = logging.StreamHandler(stdout)
    handler.setLevel(config.LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def lowercase(iterable: Iterable[str]) -> Iterable[str]:
    return type(iterable)(map(lambda x: x.lower(), iterable))
