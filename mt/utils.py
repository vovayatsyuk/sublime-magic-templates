import sublime
import json
import os

from collections import OrderedDict

PACKAGE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.isfile(PACKAGE_PATH):
    PACKAGE, _ = os.path.splitext(os.path.basename(PACKAGE_PATH))
elif os.path.isdir(PACKAGE_PATH):
    PACKAGE = os.path.basename(PACKAGE_PATH)
else:
    raise ValueError('Package is no file and no directory!')

def load_resource(path, convert_to_json=False):
    try:
        path = 'Packages/%s/templates/%s' % (PACKAGE, path.lstrip('/'))
        content = sublime.load_resource(path)
    except OSError:
        print('Not Found: ' + path)
        return None

    return json.loads(content, object_pairs_hook=OrderedDict) if convert_to_json else content