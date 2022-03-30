import sublime
import json
import yaml
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
    key = ['trigger', 'scope']

    if snippets and '@extend' in snippets:
        for project, rules in snippets['@extend'].items():
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


def load_files(project):
    files = load_resource(project + '/files.json', True)
    key = ['pattern']

    if files and '@extend' in files:
        for project, rules in files['@extend'].items():
            extend = load_files(project)
            if extend:
                for path, new_files in extend.items():
                    if path not in files:
                        files[path] = []
                    else:
                        new_files = [item for item in new_files if not exists(item, files[path], key)]

                    for file in new_files:
                        if not file['path'].startswith('/'):
                            file['path'] = '/' + project + '/files/' + file['path']

                    files[path] += new_files
        del files['@extend']
    return files


def exists(item, object, keys):
    for _item in object:
        matches = 0
        for key in keys:
            if _item[key] == item[key]:
                matches += 1
        if matches == len(keys):
            return True
    return False


def closest_file(name, path, directory=False, max_depth=20):
    """Search for the closest file
    """

    if not path:
        return None

    path = path.rstrip(os.sep)
    folders = path.split(os.sep)
    if os.path.isfile(path):
        folders.pop()
    folders.append(name)

    while max_depth > 0 and len(folders) > 2:
        max_depth -= 1
        file = os.sep.join(folders)
        if os.path.isfile(file) and os.path.getsize(file) > 0:
            if directory is True:
                return file.replace(name, '')
            else:
                return file
        else:
            del folders[-2]


def load_file(path, convert_to_json=False):
    content = None

    if path is not None:
        with open(path, 'r', encoding="utf-8") as stream:
            try:
                if path.endswith('json'):
                    string = stream.read()
                    if string:
                        content = json.loads(
                            string,
                            object_pairs_hook=OrderedDict
                        )
                elif path.endswith(('yml', 'yaml')):
                    content = yaml.safe_load(stream)
            except OSError:
                print('Load file error')

    return content
