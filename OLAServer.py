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
   exposed = True
   def GET(self):
      raise cherrypy.HTTPRedirect("/index.html")

root = Root()
groups = JSonSerializer().Load(file('groups.json', 'r').read())
parkedChannels = ParseParkedChannels(file('parked.json', 'r').read())
channelController = FadeChannelAdapter(lambda: None, ParkedChannelAdapter(parkedChannels, OLAController()))
#channelController = ParkedChannelAdapter(parkedChannels, OLAController())
groupController = GroupController(groups, channelController)
root.groups = GroupWebAdapter(groupController)

presets = json.load(file('presets.json', 'r'))
root.presets = PresetWebAdapter(presets)

print "Starting"
StartWebServer(root)
