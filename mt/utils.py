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
        path = 'Packages/%s/projects/%s' % (PACKAGE, path.lstrip('/'))
        content = sublime.load_resource(path)
    except OSError:
        print('Not Found: ' + path)
        return None

    if convert_to_json:
        content = json.loads(content, object_pairs_hook=OrderedDict)

    return content


def load_snippets(project):
    snippets = load_resource(project + '/snippets.json', True)
    key = 'trigger'

    if snippets and '@extend' in snippets:
        for project, rules in snippets['@extend'].items():
            # del snippets['@extend'][project]
            extend = load_snippets(project)
            if extend:
                for path, new_snippets in extend.items():
                    if path not in snippets:
                        snippets[path] = []
                    else:
                        new_snippets = [item for item in new_snippets if not exists(item, snippets[path], key)]

                    for snippet in new_snippets:
                        if not snippet['path'].startswith('/'):
                            snippet['path'] = '/' + project + '/snippets/' + snippet['path']

                    snippets[path] += new_snippets
        del snippets['@extend']

    return snippets


def exists(item, object, key):
    for _item in object:
        if _item[key] == item[key]:
            return True
    return False
