import datetime

class alarms(object):
    summary = ""
    time = ""

    def __init__(self, summary, time):
        self.summary = summary
        self.time = time

    def getTime(self):
        return self.time




