import array
import unittest
import copy
from ChannelController import IChannelController

class FadeChannelAdapter(IChannelController):
    def __init__(self, callback, controller):
        self._controller = controller
        self._callback = callback
        self._data = None

    def SetLevels(self, universe, data):
        if self._data is None:
            self._data = copy.deepcopy(data)

       
        while self._data != data:
            for i,val in enumerate(data):
                if self._data[i] < data[i]:
                    self._data[i] += 1
                elif self._data[i] > data[i]:
                    self._data[i] -= 1
        
            self._controller.SetLevels(universe, self._data)
            if self._callback is not None:
                self._callback()

class MockChannelController(IChannelController):
    def __init__(self):
        self.history = []
   
    def SetLevels(self, universe, data):
        self.history += [copy.deepcopy(data)]
      
            
class Test_GroupController(unittest.TestCase):
    def setUp(self):
        self._mockController = MockChannelController()
        self._fader = FadeChannelAdapter(None, self._mockController)
        
        
    def test_LevelFadesUp(self):
        self._fader.SetLevels(1, array.array('B', [0, 0]))

        self._fader.SetLevels(1, array.array('B', [3, 0]))
        
        expected = [array.array('B', [1, 0]),
                    array.array('B', [2, 0]),
                    array.array('B', [3, 0])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_LevelFadesDown(self):
        self._fader.SetLevels(1, array.array('B', [0, 3]))

        self._fader.SetLevels(1, array.array('B', [0, 0]))

        expected = [array.array('B', [0, 2]),
                    array.array('B', [0, 1]),
                    array.array('B', [0, 0])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_BothDirections(self):
        self._fader.SetLevels(1, array.array('B', [10, 50]))

        self._fader.SetLevels(1, array.array('B', [15, 40]))

        expected = [array.array('B', [11, 49]),
                    array.array('B', [12, 48]),
                    array.array('B', [13, 47]),
                    array.array('B', [14, 46]),
                    array.array('B', [15, 45]),
                    array.array('B', [15, 44]),
                    array.array('B', [15, 43]),
                    array.array('B', [15, 42]),
                    array.array('B', [15, 41]),
                    array.array('B', [15, 40])]
       
        self.assertEqual(expected, self._mockController.history)

if __name__ == "__main__":
    unittest.main();       