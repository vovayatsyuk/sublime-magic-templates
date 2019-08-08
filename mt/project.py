import os
import sublime

from .filters import *
from .utils import load_resource
from .utils import closest_file
from .utils import load_file


class Project:
    def __init__(self, app):
        self.app = app
        self._type = None

    def root(self):
        if self.app.composer.path():
            return self.app.composer.path().replace('/composer.json', '')
        else:
            return os.path.dirname(self.app.filepath)

    def code(self):
        psr4key = self.app.file.psr4key()
        if psr4key:
            return psr4key.replace('\\', '_').strip('_')
        else:
            return ''

    def vendor(self):
        psr4key = self.app.file.psr4key()
        if psr4key:
            return kebabcase(psr4key.split('\\')[0])
        else:
            return self.app.composer.vendor()

    def project(self):
        psr4key = self.app.file.psr4key()
        if psr4key:
            parts = psr4key.split('\\')
            if len(parts) > 1:
                return kebabcase(parts[1])
        else:
            project = self.app.composer.project()
            removes = [
                'magento2-',
                'magento-2-',
                'module-',
                '-extension',
                '-magento-2',
                'magento-',
                'magento1-'
            ]
            for string in removes:
                project = project.replace(string, '')
            return project

    def type(self):
        if self._type is not None:
            return self._type

        self._type = self.guess_type_by_file()

        if self._type is None and self.app.composer.path():
            self._type = self.guess_type_by_composer()

        if self._type is None:
            self._type = self.guess_type_by_contents()

        return self._type

    def guess_type_by_file(self):
        settings = sublime.load_settings('MagicTemplates.sublime-settings')
        for project in settings.get('projects'):
            manifest = load_resource(project + '/manifest.json', True)
            for file in manifest.get('files', []):
                for filename in file:
                    path = closest_file(filename, self.app.filepath)
                    contents = load_file(path)
                    if contents:
                        rules = file.get(filename)
                        for rule in rules:
                            match = True
                            for prop in rule:
                                compare = contents.get(prop, None)
                                if compare is None:
                                    match = False
                                elif rule[prop] not in compare:
                                    match = False
                            if match is True:
                                return project
        return None

    def guess_type_by_contents(self):
        view = sublime.active_window().active_view()
        settings = sublime.load_settings('MagicTemplates.sublime-settings')
        for project in settings.get('projects'):
            manifest = load_resource(project + '/manifest.json', True)
            for rules in manifest.get('view', []):
                match = True
                for prop in rules:
                    value = rules.get(prop)
                    if prop == 'contents':
                        values = value.split(' && ')
                        for regex in values:
                            inverted = False
                            if regex.startswith('!'):
                                inverted = True
                                regex = regex[1:]
                            region = view.find(regex, sublime.IGNORECASE)
                            if (not inverted and
                                    (region is None or
                                        region.a == region.b)):
                                match = False
                            elif (inverted and
                                    (region is not None and
                                        region.a != region.b)):
                                match = False
                    elif prop == 'scope':
                        if value not in view.scope_name(0):
                            match = False
                    else:
                        match = False
                if match is True:
                    return project
        return None

    def guess_type_by_composer(self):
        settings = sublime.load_settings('MagicTemplates.sublime-settings')
        for project in settings.get('projects'):
            manifest = load_resource(project + '/manifest.json', True)
            fileset = manifest.get('files', [])
            for file in fileset:
                for rules in file.get('composer.json', []):
                    match = True
                    for prop in rules:
                        compare = self.app.composer.data(prop)
                        if compare is None:
                            match = False
                        elif rules.get(prop) not in compare:
                            match = False
                    if match is True:
                        return project
        return None
