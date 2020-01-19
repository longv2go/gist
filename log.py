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
            "format": "%(asctime)s %(levelname)s [%(process)d] %(message)s"
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

def info(msg, *args, **kwargs):
    __logger.info(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    __logger.debug(msg, *args, **kwargs)

def warn(msg, *args, **kwargs):
    __logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    __logger.error(msg, *args, **kwargs)


if __name__ == '__main__':
    info('info')
    warn('warn')
    error('error')
    debug('debug')