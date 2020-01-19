# -*- coding: utf-8 -*-

import logging
import logging.config

__LOGGER_CONFIG = {
    "version": 1,
    "loggers": {
        "common": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": [
                "console",
                "common"
            ]
        },
        "loadTest": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": [
                "loadTest"
            ]
        }
    },
    "formatters": {
        "simpleformat": {
            "format": "%(asctime)s %(levelname)s %(process)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "simpleformat",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG"
        },
        "common": {
            "formatter": "simpleformat",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": ".log_common.log",
            "mode": "w"
        },
        "loadTest": {
            "formatter": "simpleformat",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": ".log_loadTest.log",
            "mode": "w"
        }
    }
}

# load logging config and init __logger
logging.config.dictConfig(__LOGGER_CONFIG)
__logger = logging.getLogger('common')

# ------ end public methods ------

def setLogger(name):
    global __logger
    try:
        __logger = logging.getLogger(name)
    except Exception as e:
        print(e)

def info(msg):
    __logger.info(msg)

def debug(msg):
    __logger.info(msg)

def warn(msg):
    __logger.warning(msg)

def error(msg):
    __logger.error(msg)


if __name__ == '__main__':
    info('info')
    warn('warn')
    error('error')
    debug('debug')