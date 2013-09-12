import time
from Group import *
from GroupSerializer import *
from GroupController import *
from ChannelController import *
from GroupWebAdapter import *
from ParkedChannel import *
from ParkedChannelAdapter import *
from PresetWebAdapter import *
from FadeChannelAdapter import *
from ThreadControllerAdapter import *
from MockClientWrapperFactory import *

class Root(object):
    pass

def StartServer(ClientWrapperFactory):
    root = Root()
    groups = JSonSerializer().Load(file('groups.json', 'r').read())
    parkedChannels = ParseParkedChannels(file('parked.json', 'r').read())
    channelController = FadeChannelAdapter(ParkedChannelAdapter(parkedChannels, ThreadControllerAdapter(ClientWrapperFactory)))
    groupController = GroupController(groups, channelController)
    root.groups = GroupWebAdapter(groupController)

    presets = json.load(file('presets.json', 'r'))
    root.presets = PresetWebAdapter(presets)

    StartWebServer(root)