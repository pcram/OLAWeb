import time
import datetime

class MockClient:
    _lastData = None

    def SendDmx(self, universe, data, callback):
        if self._lastData != data:
            print "Universe: " + str(universe) + ", Data: " + ','.join("%x" % x for x in data)
            self._lastData = data
        callback(None)

class MockClientWrapper:
    _nextTime = datetime.datetime.max
    _nextCallback = None
    _mockClient = MockClient()

    def Client(self):
        return self._mockClient

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


