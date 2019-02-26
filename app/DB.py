from threading import Thread
from queue import Queue
from sqlite3 import OperationalError
import sqlite3
import traceback


# DB queue executor implementation.
class DB(Thread):
    __instance = None

    @staticmethod
    def getiInstance():
        if DB.__instance is None:
            DB()
        return DB.__instance

    def __init__(self):
        if DB.__instance is not None:
            raise Exception("Class is singleton, use '.getiInstance()'.")
        else:
            DB.__instance = self

        Thread.__init__(self)

        self.connect("data.db")
        self.queue = Queue()

    def connect(self, path):
        if self.is_alive() is False:
            self.path = path
            self.daemon = True
            self.start()

    def run(self):

        db = sqlite3.connect(self.path)
        cursor = db.cursor()

        while True:
            req, arg, out, func = self.queue.get()

            if func == -1:
                commit = False
                res = []

                if not req.upper().startswith("SELECT"):
                    commit = True
                try:
                    cursor.execute(req, arg)
                    for row in cursor.fetchall():
                        res.append(row)

                    if len(res) is 0:
                        out.put(None)
                    else:
                        out.put(res)

                    if commit:
                        db.commit()
                except OperationalError:
                    traceback.print_exc()
                    out.put(None)
            else:
                break

        db.close()

    def exec(self, req, arg=None):
        out = Queue()
        self.queue.put((req, arg or tuple(), out, -1))
        return out.get()

    def close(self):
        self.queue.put("exit;")
