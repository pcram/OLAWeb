import time
import datetime

class MockClientWrapper:
    _nextTime = datetime.datetime.max
    _nextCallback = None

    def Client(self):
        return MockClient()

    def AddEvent(self, time, callback):
        self._nextTime = datetime.datetime.now() + datetime.timedelta(milliseconds = time)
        self._nextCallback = callback

    def Run(self):
        while True:
            if datetime.datetime.now() >= self._nextTime:
                callback = self._nextCallback
                self._nextTime = datetime.datetime.max
                self._nextCallback = None
                callback()


class MockClient:
    def SendDmx(self, universe, data, callback):
        print "Universe: " + str(universe) + ", Data: " + ','.join(str(x) for x in data)
        callback(None)
