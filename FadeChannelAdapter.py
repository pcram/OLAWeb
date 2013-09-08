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
                    self._data[i] = min(data[i], self._data[i] + 1)
                elif self._data[i] > data[i]:
                    self._data[i] = max(data[i], self._data[i] - 1)
        
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

        self._fader.SetLevels(1, array.array('B', [13, 0]))
        
        expected = [array.array('B', [5, 0]),
                    array.array('B', [10, 0]),
                    array.array('B', [13, 0])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_LevelFadesDown(self):
        self._fader.SetLevels(1, array.array('B', [0, 15]))

        self._fader.SetLevels(1, array.array('B', [0, 3]))

        expected = [array.array('B', [0, 10]),
                    array.array('B', [0, 5]),
                    array.array('B', [0, 3])]
       
        self.assertEqual(expected, self._mockController.history)

    def test_BothDirections(self):
        self._fader.SetLevels(1, array.array('B', [10, 50]))

        self._fader.SetLevels(1, array.array('B', [17, 38]))

        expected = [array.array('B', [15, 45]),
                    array.array('B', [17, 40]),
                    array.array('B', [17, 38])]
       
        self.assertEqual(expected, self._mockController.history)

if __name__ == "__main__":
    unittest.main();       
