from Group import *
from ChannelController import *
import array
import unittest

class IGroupController(object):
    def SetLevel(self, id, newLevel):
        pass

class GroupController(IGroupController):
    def __init__(self, groups, parkList, channelController):
        self.groups = groups;
        self.channelController = channelController
        self._parkedChannels = parkList
        for group in self.groups:
            group.level = 100

        self._SendUpdate()

    def SetLevel(self, id, newLevel):
        for group in self.groups:
            if group.id == int(id):
                group.level = int(newLevel)

        self._SendUpdate()

    def SetChannelList(self, id, channels):
        for group in self.groups:
            if group.id == int(id):
                group.channels = channels

        self._SendUpdate()

    def _SendUpdate(self):
        data = array.array('B')

        for channel in range(1, 256):
            maxValue = 0
            if channel in self._parkedChannels.keys():
                maxValue = self._parkedChannels[channel]
            else:
                for group in self.groups:
                    if group.channels.count(channel) > 0:
                        maxValue = max(maxValue, group.level)
        
            data.append(maxValue * 255 / 100)
        
        self.channelController.SetLevels(1, data)

    def NewGroup(self):
        maxid = 0
        for group in self.groups:
            maxid = max(maxid, group.id)
        
        self.groups.append(Group(maxid + 1, "New Group", []))

    def Delete(self, id):
        self.groups = [x for x in self.groups if x.id != int(id)]

    def SetParkList(self, parkList):
        self._parkedChannels = parkList
        self._SendUpdate()

class MockChannelController(IChannelController):
    def SetLevels(self, universe, data):
        self.data = data

class Test_GroupController(unittest.TestCase):
    def percentToAbsolute(self, percent):
        return percent * 255 / 100

    def setUp(self):
        groups = [Group(1, "Stage", [1,2,3]), Group(2, "Center", [2]), Group(3, "Parked", [50])]
        self.mockChannelController = MockChannelController()
        self.parkList = {50 : 100, 60: 75}
        self.controller = GroupController(groups, self.parkList, self.mockChannelController);

    def test_NewLevelSaved(self):
        self.controller.SetLevel(1, 10)
        self.assertEqual(10, self.controller.groups[0].level)

    def test_ChannelsUpdated(self):
        self.controller.SetLevel(1, 10)
        self.assertEqual(self.percentToAbsolute(10), self.mockChannelController.data[0])
        self.assertEqual(self.percentToAbsolute(10), self.mockChannelController.data[2])
        self.assertEqual(0, self.mockChannelController.data[3])

    def test_ConflictPicksHighest(self):
        self.controller.SetLevel(1, 50)
        self.controller.SetLevel(2, 10)
        self.assertEqual(self.percentToAbsolute(50), self.mockChannelController.data[1])
        
    def test_UpdateChannels(self):
        self.controller.SetChannelList(2,[4,5,6,7])
        self.assertEqual(self.controller.groups[1].channels, [4,5,6,7])

    def test_UpdateChannelsSendsImmediateUpdate(self):
        self.controller.SetLevel(1, 50)
        self.assertEqual(self.percentToAbsolute(50), self.mockChannelController.data[0])
        self.assertEqual(self.percentToAbsolute(0), self.mockChannelController.data[9])
        self.controller.SetChannelList(1, [10])
        self.assertEqual(self.percentToAbsolute(0), self.mockChannelController.data[0])
        self.assertEqual(self.percentToAbsolute(50), self.mockChannelController.data[9])

    def test_ParkedChannelsSet(self):
        self.assertEqual(self.percentToAbsolute(100), self.mockChannelController.data[49])
        self.assertEqual(self.percentToAbsolute(75), self.mockChannelController.data[59])

    def test_ParkedChannelsDontGoHigher(self):
        self.controller.SetLevel(3, 100)
        self.assertEqual(self.percentToAbsolute(75), self.mockChannelController.data[59])

    def test_ParkedChannelsDontGoLower(self):
        self.controller.SetLevel(3, 0)
        self.assertEqual(self.percentToAbsolute(75), self.mockChannelController.data[59])
        self.assertEqual(self.percentToAbsolute(100), self.mockChannelController.data[49])
 
    def test_UpdatingParkListSendsImmediately(self):
        self.controller.SetParkList({55 : 100, 65 : 75})
        
        self.assertEqual(self.percentToAbsolute(100), self.mockChannelController.data[54])
        self.assertEqual(self.percentToAbsolute(75), self.mockChannelController.data[64])

        self.assertEqual(self.percentToAbsolute(0), self.mockChannelController.data[59])
        self.assertEqual(self.percentToAbsolute(100), self.mockChannelController.data[49])

        self.controller.SetLevel(3, 50)
        self.assertEqual(self.percentToAbsolute(50), self.mockChannelController.data[49])
 
if __name__ == "__main__":
    unittest.main();       