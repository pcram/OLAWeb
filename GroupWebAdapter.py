import json
import copy
import os
import cherrypy
from GroupSerializer import *

class GroupWebAdapter(object):
    exposed = True

    def __init__(self, controller):
        self.controller = controller
    
    def _ListAllGroups(self):
        return json.dumps(self.controller.groups, cls=GroupsWithLevels)

    def GET(self, *vpath, **params):
        if len(vpath) == 0:
            return self._ListAllGroups()
        else:
            return self._GroupDetails(int(vpath[0]))
            
    def _GroupDetails(self, id):
        for group in self.controller.groups:
            if group.id == id:
                return json.dumps(group, cls=GroupsFullDetails)


    def PUT(self, id, *path, **params):
        if 'level' in params:
            self.controller.SetLevel(id, params['level'])
        
        if 'channels' in params:
            if len(params['channels']) == 0:
                self.controller.SetChannelList(id, [])
            else:
                self.controller.SetChannelList(id, [int(i) for i in params['channels'].split(",")])
        
            self.Save()

        if 'name' in params:
            for group in self.controller.groups:
                if group.id == int(id):
                    group.name = params['name']

            self.Save()

    def POST(self):
        self.controller.NewGroup()
        self.Save()

    def DELETE(self, id):
        self.controller.Delete(id)
        self.Save()

    def Save(self):
        file('groups.json', 'w').write(JSonSerializer().Save(self.controller.groups))


class GroupsFullDetails(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
        
    
class GroupsWithLevels(json.JSONEncoder):
    def default(self, obj):
        dict = copy.deepcopy(obj.__dict__)
        dict.pop('channels')
        return dict

def StartWebServer(root):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8000,
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(current_dir, 'static'),
        },
    
    }

    cherrypy.quickstart(root, '/', conf)
