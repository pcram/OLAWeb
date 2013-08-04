from Group import *
from GroupSerializer import *
from GroupController import *
from ChannelController import *
from WebAdapter import *
from ParkedChannel import *
from ParkedChannelAdapter import *

class Root(object):
    pass

root = Root()
groups = JSonSerializer().Load(file('groups.json', 'r').read())
parkedChannels = ParseParkedChannels(file('parked.json', 'r').read())
channelController = ParkedChannelAdapter(parkedChannels, TextChannelController())
groupController = GroupController(groups, channelController)
root.groups = WebAdapter(groupController)

StartWebServer(root)