# -*- coding: UTF-8 -*-

import cherrypy
import config
import re
import json
from TestFactory import TestFactory, TestUser
from app import render


testfact = TestFactory()


def errorPage(status, message, **kwargs):
    return render("error.html", title=config.app["title"], status=status, message=message, kwargs=kwargs)


class Index:
    __namepat = re.compile(r"^[a-zA-Z]*$")
    __idpat = re.compile(r"^\d{8}$")

    def __init__(self):
        self.user = User()

    # Manage REST style URL's.
    def _cp_dispatch(self, vpath):

        # /test/<uuid>
        if len(vpath) == 2:
            action = vpath.pop(0)

            if action == "test":
                cherrypy.request.params["uid"] = vpath.pop(0)
                return self.user.test

        return vpath

    @cherrypy.expose
    def index(self):
        return render("index/index.html")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def jump(self, std_famname, std_id):

        if self.__namepat.match(std_famname):
            if self.__idpat.match(std_id):

                user = TestUser()
                user.user = std_famname
                user.id = std_id

                uid = testfact.regUser(user)

                if uid is None:
                    return {"status": False, "msg": "User not exist."}
                elif uid is 0:
                    return {"status": False, "msg": "New test for this user is not available."}

                return {"status": True, "id": str(uid)}
            else:
                return {"status": False, "msg": "Incorrect id format."}
        else:
            return {"status": False, "msg": "Incorrect surname format."}


class User:

    @cherrypy.expose
    def test(self, uid, **kw):
        answer = kw.pop("answer[]", [])

        test = testfact.getTest(uid)

        if len(answer) is not 0:
            test.registerQAnswer(answer)
            cherrypy.response.headers["Content-Type"] = "application/json"

            if test.complete:
                return json.dumps({"status": True, "done": True}).encode("UTF-8")

            return json.dumps({
                "status": True,
                "question": test.question,
                "answers": test.answers,
                "idx": test.qidx,
            }).encode("UTF-8")

        data = {
            "uid": test.uid,
            "user": test.user,
            "available": test.available,
        }

        if test.IsEnded():
            return render("user/test.html", data)
        elif test.complete:
            data = {
                "complete": True,
                "idx": test.qidx,
                "tidx": test.getQCount(),
                "correct": test.correct,
                "result": test.getResult(),
                **data
            }
            return render("user/test.html", data)

        data = {
            "timestamp": test.timestamp,
            "available": test.available,
            "question": test.question,
            "answers": test.answers,
            "idx": test.qidx,
            "tidx": test.getQCount(),
            **data
        }

        return render("user/test.html", data)
