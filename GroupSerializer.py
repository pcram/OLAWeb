import unittest
import json
import copy
from Group import *

class ISerializer(object):
    def Load(self, json):
        pass

    def Save(self, groups):
        pass

class GroupsWithChannels(json.JSONEncoder):
    def default(self, obj):
        dict = copy.deepcopy(obj.__dict__)
        dict.pop('level')
        return dict

class JSonSerializer(ISerializer):
    def Load(self, jsonText):
        groups = []
        for entry in json.loads(jsonText):
            groups.append(Group(int(entry['id']), entry['name'], entry['channels']))

        return groups

    def Save(self, groups):
        return json.dumps(groups, cls=GroupsWithChannels, indent=4)



class Test_JSonSerializer(unittest.TestCase):

    def test_Load(self):
        groups = JSonSerializer().Load("""[{"channels": [1, 2, 3], "id": 1, "name": "Stage"}, {"channels": [4, 5, 6], "id": 2, "name": "House"}]""")
        
        self.assertEqual(len(groups), 2)
        self.assertEqual(1, groups[0].id)
        self.assertEqual("Stage", groups[0].name)
        self.assertEqual([1,2,3], groups[0].channels)

    def test_Save(self):
        serialized = JSonSerializer().Save([Group(1, "One", [1,2,3]), Group(2, "Two", [4,5,6])])
        self.assertEqual("""[{"channels":[1,2,3],"id":1,"name":"One"},{"channels":[4,5,6],"id":2,"name":"Two"}]""", ''.join(serialized.split()))

if __name__ == "__main__":
    unittest.main();