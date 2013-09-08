from ola.ClientWrapper import ClientWrapper
from ChannelController import IChannelController
import threading
import Queue
import array

_cache = {}

def DmxSent(state):
    pass

def SendDMXFrame():
    _wrapper.AddEvent(100, SendDMXFrame)    
    client = _wrapper.Client()
    for universe in _cache.keys():     
        client.SendDmx(universe, _cache[universe], DmxSent)



def WorkerThread():
    global _wrapper
    _wrapper = ClientWrapper()
    client = _wrapper.Client()
    _wrapper.AddEvent(100, SendDMXFrame)
    _wrapper.Run()

class OLAController(IChannelController):
    def __init__(self):
        thread = threading._start_new_thread(WorkerThread, ())

    def SetLevels(self, universe, data):
	global _cache
        _cache[universe] = data
      
  
