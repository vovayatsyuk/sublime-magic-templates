import os
import json
import sublime

from .filters import *

class Composer:
    def __init__(self, app):
        self.app = app
        self.file_path = app.filepath
        self.path = None
        self.data = None
        self.psr4key = None
        self.vendor = 'Unknown'
        self.module = 'Unknown'

    def get_file(self):
        """
        Try to locate composer,json file.
        1. If '/vendor/' in file_path, return path/to/vendor/xxx/xxx/composer.json
        2. Search for composer.json file in each of the folders beginning
            from the deepest path.
        """

        if self.path is not None:
            return self.path

        vendor_dir = '/vendor/'
        if vendor_dir in self.file_path:
            root, module_path = self.file_path.split(vendor_dir)
            self.vendor, self.module, rest = module_path.split(os.sep, 2)
            composer = os.sep.join([root, 'vendor', self.vendor, self.module, 'composer.json'])
            if os.path.isfile(composer):
                self.path = composer
                return composer
        else:
            root = sublime.active_window().extract_variables().get('folder')
            min_depth = root.count('/') + 1
            folders = self.file_path.split(os.sep)
            folders.pop() # remove filename
            folders.append('composer.json')
            while len(folders) > min_depth:
                composer = os.sep.join(folders)
                if os.path.isfile(composer):
                    self.path = composer
                    return composer
                else:
                    del folders[len(folders) - 2] # remove last folder

        print('composer.json not found')
        return None

    def load(self):
        composer = self.get_file()
        try:
            with open(composer) as file:
                self.data = json.loads(file.read())
        except:
            self.data = {
                'name': self.vendor + '/' + self.module,
                'autoload': {
                    'psr-4': {
                        camelcase(self.vendor) + '\\' + camelcase(self.module): ''
                    }
                }
            }

    def get_name(self):
        return self.get_data('name')

    def get_vendor_folder(self):
        return self.get_name().split('/')[0]

    def get_project_folder(self):
        return self.get_name().split('/')[1]

    def get_vendor(self):
        psr4key = self.app.env.psr4key()
        if psr4key:
            return kebabcase(psr4key.split('\\')[0])

        # Logic below is used, when composer is not found
        return self.get_name().split('/')[0]

    def get_project(self):
        psr4key = self.app.env.psr4key()
        if psr4key:
            parts = psr4key.split('\\')
            if len(parts) > 1:
                return kebabcase(parts[1])

        # Logic below is used, when composer is not found
        project = self.get_project_folder()
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

    def get_type(self):
        return self.get_data('type')

    def get_psr4(self):
        return self.get_data('autoload.psr-4')

    def get_data(self, key = ''):
        if self.data is None:
            self.load()
        if key == '':
            return self.data
        if '.' in key:
            data = self.get_by_path(key);
        else:
            data = self.get_by_key(key);
        return data

    def get_by_key(self, key):
        return self.data.get(key, None)

    def get_by_path(self, path):
        keys = path.split('.')
        data = self.data
        for key in keys:
            if data is None:
                break
            data = data.get(key, None)
        return data
