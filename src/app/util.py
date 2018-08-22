import logging
from sys import stdout
from time import gmtime

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
