import urllib.request
import json
from _constants import *


def parse_version(vstr):
    vstrs = vstr.lstrip('v').split('.')
    return [int(v) for v in vstrs]


def check_for_updates():
    try:
        response = urllib.request.urlopen(
            "https://api.github.com/repos/The-Orange-Toolbox/BSPReveal/releases/latest")
        meta = json.loads(response.read())
        latest_version = parse_version(meta['tag_name'])
        current_version = parse_version(VERSION)

        for i in range(len(current_version)):
            if current_version[i] > latest_version[i]:
                break
            if current_version[i] < latest_version[i]:
                print("A new version of " + NAME + " is available")
                print("https://github.com/The-Orange-Toolbox/BSPReveal/releases\n")
    except:
        pass
