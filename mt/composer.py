import os
import json
import sublime

from .filters import *

class Composer:
    def __init__(self, app):
        self.app = app
        self._filepath = app.filepath
        self._path = None
        self._data = None
        self._vendor = 'Unknown'
        self._module = 'Unknown'

    def path(self):
        """
        Try to locate composer,json file.
        1. If '/vendor/' in file_path, return path/to/vendor/xxx/xxx/composer.json
        2. Search for composer.json file in each of the folders beginning
            from the deepest path.
        """

        if self._path is not None:
            return self._path

        vendor_dir = '/vendor/'
        if vendor_dir in self._filepath:
            root, module_path = self._filepath.split(vendor_dir)
            self._vendor, self._module, rest = module_path.split(os.sep, 2)
            composer = os.sep.join([root, 'vendor', self._vendor, self._module, 'composer.json'])
            if os.path.isfile(composer):
                self._path = composer
                return composer
        else:
            root = sublime.active_window().extract_variables().get('folder')
            min_depth = root.count('/') + 1
            folders = self._filepath.split(os.sep)
            folders.pop() # remove filename
            folders.append('composer.json')
            while len(folders) > min_depth:
                composer = os.sep.join(folders)
                if os.path.isfile(composer):
                    self._path = composer
                    return composer
                else:
                    del folders[len(folders) - 2] # remove last folder

        print('composer.json not found')
        return None

    def load(self):
        composer = self.path()
        try:
            with open(composer) as file:
                self._data = json.loads(file.read())
        except:
            self._data = {
                'name': self._vendor + '/' + self._module,
                'autoload': {
                    'psr-4': {
                        camelcase(self._vendor) + '\\' + camelcase(self._module): ''
                    }
                }
            }

    def name(self):
        return self.data('name')

    def vendor_folder(self):
        return self.name().split('/')[0]

    def project_folder(self):
        return self.name().split('/')[1]

    def vendor(self):
        psr4key = self.app.env.psr4key()
        if psr4key:
            return kebabcase(psr4key.split('\\')[0])

        # Logic below is used, when composer is not found
        return self.name().split('/')[0]

    def project(self):
        psr4key = self.app.env.psr4key()
        if psr4key:
            parts = psr4key.split('\\')
            if len(parts) > 1:
                return kebabcase(parts[1])

        # Logic below is used, when composer is not found
        project = self.project_folder()
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
        return self.data('type')

    def psr4(self):
        return self.data('autoload.psr-4')

    def data(self, key = ''):
        if self._data is None:
            self.load()
        if key == '':
            return self._data
        if '.' in key:
            data = self.get_by_path(key);
        else:
            data = self.get_by_key(key);
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
