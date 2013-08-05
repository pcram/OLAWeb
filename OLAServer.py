import time
from Group import *
from GroupSerializer import *
from GroupController import *
from OLAController import *
from GroupWebAdapter import *
from ParkedChannel import *
from ParkedChannelAdapter import *
from PresetWebAdapter import *
from FadeChannelAdapter import *

class Root(object):
    pass

root = Root()
groups = JSonSerializer().Load(file('groups.json', 'r').read())
parkedChannels = ParseParkedChannels(file('parked.json', 'r').read())
channelController = FadeChannelAdapter(lambda: time.sleep(0.01), ParkedChannelAdapter(parkedChannels, OLAController()))
groupController = GroupController(groups, channelController)
root.groups = GroupWebAdapter(groupController)

presets = json.load(file('presets.json', 'r'))
root.presets = PresetWebAdapter(presets)

StartWebServer(root)