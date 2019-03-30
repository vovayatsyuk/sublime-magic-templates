import os
import json
import sublime

from .filters import *
from collections import OrderedDict


class Composer:
    def __init__(self, app):
        self.app = app
        self._path = None
        self._data = None
        self._vendor_dir = 'Unknown'
        self._module_dir = 'Unknown'

    def path(self):
        """
        Try to locate composer.json file.
        1. If '/vendor/' in file_path,
            return path/to/vendor/xxx/xxx/composer.json
        2. Search for composer.json file in each of the folders beginning
            from the deepest path.
        """

        if self._path is not None:
            return self._path

        vendor_dir = '/vendor/'
        if vendor_dir in self.app.filepath:
            root, module_path = self.app.filepath.split(vendor_dir)
            self._vendor_dir, self._module_dir, rest = module_path.split(os.sep, 2)
            composer = os.sep.join([root, 'vendor', self._vendor_dir, self._module_dir, 'composer.json'])
            if os.path.isfile(composer) and os.path.getsize(composer) > 0:
                self._path = composer
                return composer

        root = sublime.active_window().extract_variables().get('folder')
        if root is None:
            min_depth = 5
        else:
            min_depth = root.count('/') + 1

        folders = self.app.filepath.split(os.sep)
        # remove filename
        folders.pop()
        folders.append('composer.json')
        while len(folders) > min_depth:
            composer = os.sep.join(folders)
            if os.path.isfile(composer) and os.path.getsize(composer) > 0:
                self._path = composer
                return composer
            else:
                # remove last folder
                del folders[len(folders) - 2]

        return None

    def load(self):
        composer = self.path()
        try:
            with open(composer) as file:
                self._data = json.loads(
                    file.read(),
                    object_pairs_hook=OrderedDict
                )
        except:
            self._data = {
                'name': self._vendor_dir + '/' + self._module_dir,
                'autoload': {
                    'psr-4': {
                        camelcase(self._vendor_dir) + '\\' + camelcase(self._module_dir) + '\\': ''
                    }
                }
            }

    def name(self):
        return self.data('name')

    def vendor(self):
        return self.name().split('/')[0]

    def project(self):
        return self.name().split('/')[1]

    def type(self):
        return self.data('type')

    def psr4(self):
        return self.data('autoload.psr-4')

    def data(self, key=''):
        if self._data is None:
            self.load()
        if key == '':
            return self._data
        if '.' in key:
            data = self.get_by_path(key)
        else:
            data = self.get_by_key(key)
        return data

    def get_by_key(self, key):
        return self._data.get(key, None)

    def get_by_path(self, path):
        keys = path.split('.')
        data = self._data
        for key in keys:
            if data is None:
                break
            data = data.get(key, None)
        return data
