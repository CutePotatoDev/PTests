from DB import DB
from datetime import datetime
import TestFactory


class Test:
    def __init__(self, uid):
        self.db = DB.getiInstance()

        self.uid = uid
        self.user = ""
        self.timestamp = 0
        self.available = 0
        self.complete = False

        self.question = ""
        self.answers = []
        self.aidx = []
        self.correct = 0

        data = self.db.exec("SELECT User, StartTime, Active, Questions FROM Users INNER JOIN Tests ON Id = UserId WHERE Uid = ? AND Active = 1 ORDER BY StartTime DESC LIMIT 1;", (uid,))
        if data is None:
            return

        self.user = data[0][0]
        self.timestamp = int(datetime.strptime(data[0][1], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000) + TestFactory.TestFactory.TESTTIME
        self.available = data[0][2]

        self.questions = data[0][3].split(",")
        self.qidx = 0

        self.__getQData()

    def IsEnded(self):
        if int(datetime.now().timestamp() * 1000) > self.timestamp:
            self.available = False
            return True
        return False

    def getQCount(self):
        return len(self.questions)

    def getResult(self):
        return (10 / TestFactory.TestFactory.QCOUNT) * self.correct

    def __getQData(self):
        if len(self.questions) is 0:
            return
        elif len(self.questions) is self.qidx:
            self.complete = True
            self.db.exec("UPDATE Tests Set Result = ? WHERE Uid = ?;", (self.getResult(), self.uid))
            return

        self.answers = []
        self.aidx = []

        self.question = self.db.exec("SELECT Question FROM Questions WHERE Id = ?;", (self.questions[self.qidx],))[0][0]
        answers = self.db.exec("SELECT Answer, Correct FROM Answers WHERE QId = ? ORDER BY RANDOM();", (self.questions[self.qidx],))

        for idx, row in enumerate(answers):
            self.answers.append(row[0])

            if row[1] is 1:
                self.aidx.append(idx)

        self.qidx += 1

    def registerQAnswer(self, idx):
        if isinstance(idx, list) is False:
            idx = [idx]

        if all(int(elem) in self.aidx for elem in idx):
            self.correct += 1

        self.__getQData()
