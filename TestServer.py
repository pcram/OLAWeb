from Group import *
from GroupSerializer import *
from GroupController import *
from ChannelController import *
from WebAdapter import *
from ParkedChannel import *

class Root(object):
    pass

root = Root()
groups = JSonSerializer().Load(file('groups.json', 'r').read())
parkedChannels = ParseParkedChannels(file('parked.json', 'r').read())
root.groups = WebAdapter(GroupController(groups, parkedChannels, TextChannelController()))

StartWebServer(root)