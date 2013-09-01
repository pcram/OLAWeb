from ola.ClientWrapper import ClientWrapper
from ChannelController import IChannelController
import threading
import Queue
import array

_queue = Queue.Queue()

def DmxSent(state):
    data = _queue.get()
    client = _wrapper.Client()
    client.SendDmx(data[0], data[1], DmxSent)

def SendDMXFrame():
    
    client = _wrapper.Client()
    for universe in _universeData:     
        client.SendDmx(universe, _universeData[universe], DmxSent)


def WorkerThread():
    global _wrapper
    _wrapper = ClientWrapper()
    client = _wrapper.Client()

    client.SendDmx(1, array.array('B'), DmxSent)
    _wrapper.Run()

class OLAController(IChannelController):
    def __init__(self):
        thread = threading._start_new_thread(WorkerThread, ())

    def SetLevels(self, universe, data):
        _queue.put((universe, data))
      
  
