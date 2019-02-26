# -*- coding: UTF-8 -*-

import os
import cherrypy
import config
import logging.config
from jinja2 import FileSystemLoader, Environment

__engine = Environment(loader=FileSystemLoader(os.path.join(config.path, "./view")))

cherrypy.config.update(config="app.conf")
logging.config.dictConfig(config.log_config)


def render(template, *args, **kwargs):
    template = __engine.get_template("page/" + template)
    return template.render(*args, **kwargs)


import controller

cherrypy.config.update({"error_page.default": controller.errorPage})
cherrypy.tree.mount(controller.Index(), "/", config="app.conf")
