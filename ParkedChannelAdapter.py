import unittest
import array
import copy
from ChannelController import IChannelController

class ParkedChannelAdapter(IChannelController):
    def __init__(self, parkList, channelController):
        self._parkedChannels = parkList
        self._channelController = channelController


    def SetLevels(self, universe, data):
        newdata = copy.deepcopy(data)
        for channel in range(1, 256):
           if channel in self._parkedChannels.keys():
                newdata[channel] = self._parkedChannels[channel] * 255 / 100

        self._channelController.SetLevels(universe, newdata)

class MockChannelController(IChannelController):
    def SetLevels(self, universe, data):
        self.data = data

class Test_GroupController(unittest.TestCase):
    def setUp(self):
        self.parkedChannels = {50 : 100, 60: 75}
        self.mockChannelController = MockChannelController()
        self.controller = ParkedChannelAdapter(self.parkedChannels, self.mockChannelController)

    def test_ParkedChannelsDontGoHigher(self):
        data = array.array('B', [0 for x in range(0,255)])
        data[60] = 255;
        self.controller.SetLevels(1, data)
        self.assertEqual(191, self.mockChannelController.data[60])

    def test_ParkedChannelsDontGoLower(self):
        data = array.array('B', [0 for x in range(0,255)])
        data[50] = 0;
        self.controller.SetLevels(1, data)
        self.assertEqual(255, self.mockChannelController.data[50])
 
if __name__ == "__main__":
    unittest.main();       