import array
import unittest
import copy
import threading
from ChannelController import IChannelController

class FadeChannelAdapter(IChannelController):
    def __init__(self, controller):
        self._controller = controller
        self._target = {}
        self._current = {}
        self._newDataEvent = threading.Event()
        self._thread = threading._start_new_thread(self.WorkerThread, ())

    def SetLevels(self, universe, data):
        self._target[universe] = copy.deepcopy(data)
        self._newDataEvent.set()
    
    def WorkerThread(self):
        while True:
            somethingUpdated = False
            for universe in self._target.keys():
                if not self._current.has_key(universe):
                    self._current[universe] = copy.deepcopy(self._target[universe])
                    self._controller.SetLevels(universe, self._current[universe])
                    somethingUpdated = True
                else:
                    if self.Step(self._current[universe], self._target[universe]):
                        self._controller.SetLevels(universe, self._current[universe])
                        somethingUpdated = True

            if not somethingUpdated:
                self._newDataEvent.wait()

    def Step(self, current, target):
        updated = False
        for i,val in enumerate(target):
            if current[i] < target[i]:
                current[i] += 1
                updated = True
            elif current[i] > target[i]:
                current[i] -=1
                updated = True
        return updated
        

class MockChannelController(IChannelController):
    def __init__(self):
        self.history = []
   
    def SetLevels(self, universe, data):
        self.history += [copy.deepcopy(data)]
      
            
class Test_GroupController(unittest.TestCase):
    def setUp(self):
        self._mockController = MockChannelController()
        self._fader = FadeChannelAdapter(self._mockController)
        
        
    def test_LevelFadesUp(self):
        self._fader.SetLevels(1, array.array('B', [0, 0]))
        self._mockController.history = []

        self._fader.SetLevels(1, array.array('B', [3, 0]))
        
        expected = [array.array('B', [1, 0]),
                    array.array('B', [2, 0]),
                    array.array('B', [3, 0])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_LevelFadesDown(self):
        self._fader.SetLevels(1, array.array('B', [0, 6]))
        self._mockController.history = []

        self._fader.SetLevels(1, array.array('B', [0, 3]))

        expected = [array.array('B', [0, 5]),
                    array.array('B', [0, 4]),
                    array.array('B', [0, 3])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_BothDirections(self):
        self._fader.SetLevels(1, array.array('B', [10, 50]))
        self._mockController.history = []

        self._fader.SetLevels(1, array.array('B', [17, 38]))

        expected = [array.array('B', [11, 49]),
                    array.array('B', [12, 48]),
                    array.array('B', [13, 47]),
                    array.array('B', [14, 46]),
                    array.array('B', [15, 45]),
                    array.array('B', [16, 44]),
                    array.array('B', [17, 43]),
                    array.array('B', [17, 42]),
                    array.array('B', [17, 41]),
                    array.array('B', [17, 40]),
                    array.array('B', [17, 39]),
                    array.array('B', [17, 38])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_InitialCreateSetsLevels(self):
        self._fader.SetLevels(1, array.array('B', [100,100]))

        expected = [array.array('B', [100, 100])]

        self.assertEqual(expected, self._mockController.history)

if __name__ == "__main__":
    unittest.main();       
