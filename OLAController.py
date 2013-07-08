from ola.ClientWrapper import ClientWrapper
from ChannelController import IChannelController
import threading

TICK_INTERVAL = 100  # in ms
_universeData = {}

def DmxSent(state):
    if not state.Succeeded():
        print "State: " + str(state) + ". Stopping."
        wrapper.Stop()

def SendDMXFrame():
    _wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
    
    client = _wrapper.Client()
    for universe in _universeData:     
        client.SendDmx(universe, _universeData[universe], DmxSent)


def WorkerThread():
    global _wrapper
    _wrapper = ClientWrapper()
    SendDMXFrame()
    _wrapper.Run()

class OLAController(IChannelController):
    def __init__(self):
        thread = threading._start_new_thread(WorkerThread, ())

    def SetLevels(self, universe, data):
        _universeData[universe] = data

  