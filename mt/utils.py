import sublime
import json

from collections import OrderedDict

def load_resource(path, convert_to_json=False):
    try:
        content = sublime.load_resource(path)
    except OSError:
        print('Not Found: ' + path)
        return None

    return json.loads(content, object_pairs_hook=OrderedDict) if convert_to_json else content