import json

class PresetWebAdapter(object):
    exposed = True

    def __init__(self, presets):
        self._presets = presets

    def GET(self, *vpath, **params):
          return json.dumps(self._presets)
