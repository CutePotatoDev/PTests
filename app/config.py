# -*- coding: UTF-8 -*-

import os

path = os.path.abspath(os.path.dirname(__file__))

log_config = {
    "version": 1,

    "formatters": {
        "default": {
            "format": '%(message)s'
        }
    },

    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
    },

    "loggers": {
        "cherrypy": {
            "handlers": ["default"],
            "level": "INFO"
        },
        "cherrypy.access": {
            "propagate": False
        }
    }
}

app = {
    "title": "Testas"
}
