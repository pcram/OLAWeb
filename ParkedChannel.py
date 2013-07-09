import json

def ParseParkedChannels(jsonText):
    channels = {}
    for entry in json.loads(jsonText):
        channels[entry['channel']] = entry['level']

    return channels