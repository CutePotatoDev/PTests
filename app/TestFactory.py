import uuid
import cherrypy
from DB import DB
from Test import Test
from cherrypy.process.plugins import Monitor


class TestUser():
    id = -1
    user = ""


class TestFactory:
    TESTTIME = 1800000
    QCOUNT = 10

    def __init__(self):
        self.db = DB.getiInstance()

        self.testcontainer = {}

        Monitor(cherrypy.engine, self.expireTimeCheck, frequency=30).subscribe()

    # Register new user if it's still not exist.
    def regUser(self, user):
        id = self.db.exec("SELECT Available, Id FROM Users WHERE Id = ? AND User = ?;", (user.id, user.user))

        if id is None:
            return None

        if id[0][0] == 0:
            return 0

        uid = self.db.exec("SELECT Uid FROM Tests WHERE UserId = ? AND Active = 1 ORDER BY StartTime DESC LIMIT 1;", (id[0][1],))

        if uid is None:
            self.db.exec("UPDATE Users SET Available = 0 WHERE Id = ?;", (id[0][1],))
            return self.setTest(id[0][1])

        return uid[0][0]

    def setTest(self, id):
        uid = str(uuid.uuid4())
        questionsids = self.db.exec("SELECT Id FROM Questions ORDER BY RANDOM() LIMIT ?;", (TestFactory.QCOUNT,))
        questionsids = ",".join(str(row[0]) for row in questionsids)

        self.db.exec("INSERT INTO Tests (UserId, Uid, Questions) VALUES (?, ?, ?);", (id, uid, questionsids))

        return uid

    def getTest(self, uid):
        if uid not in self.testcontainer:
            self.testcontainer[uid] = Test(uid)

        return self.testcontainer[uid]

    def expireTimeCheck(self):
        self.db.exec("UPDATE Tests SET Active = 0 WHERE DATETIME(StartTime, '+30 minutes') < DATETIME('NOW', 'LOCALTIME');")
