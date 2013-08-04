from Group import *
from GroupSerializer import *
from GroupController import *
from OLAController import *
from WebAdapter import *
from ParkedChannel import *
from ParkedChannelAdapter import *
    
class Root(object):
    pass

root = Root()
groups = JSonSerializer().Load(file('groups.json', 'r').read())
parkedChannels = ParseParkedChannels(file('parked.json', 'r').read())
channelController = ParkedChannelAdapter(parkedChannels, OLAController())
groupController = GroupController(groups, channelController)
root.groups = WebAdapter(groupController)


StartWebServer(root)