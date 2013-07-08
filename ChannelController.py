class IChannelController(object):
    def SetLevels(self, universe, data):
        pass

class TextChannelController(IChannelController):
    def SetLevels(self, universe, data):
        print "Universe: " + str(universe) + ", Data: " + ','.join(str(x) for x in data)
