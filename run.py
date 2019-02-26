# -*- coding: utf-8 -*-

import app
import cherrypy


# To run -> cherryd -i run -P app
if __name__ == '__main__':
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
