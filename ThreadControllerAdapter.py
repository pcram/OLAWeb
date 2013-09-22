import threading
import Queue
import array

_cache = {}
_clientWrapperFactory = None
_dataSentEvent = threading.Event()
TICK_INTERVAL = 10

def DmxSent(state):
    _dataSentEvent.set()

def SendDMXFrame():
    _wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)    
    client = _wrapper.Client()
    for universe in _cache.keys():     
        client.SendDmx(universe, _cache[universe], DmxSent)

def WorkerThread():
    global _wrapper
    _wrapper = _clientWrapperFactory.Create()
    client = _wrapper.Client()
    _wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
    _wrapper.Run()

class ThreadControllerAdapter():
    def __init__(self, clientWrapperFactory):
        global _clientWrapperFactory
        _clientWrapperFactory = clientWrapperFactory
        thread = threading._start_new_thread(WorkerThread, ())

    def SetLevels(self, universe, data):
        global _cache, _dataSentEvent
        _dataSentEvent.clear()
        _cache[universe] = data
        _dataSentEvent.wait()
      
  
