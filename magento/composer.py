import os
import json

from .filters import *

class Composer:
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = None
        self.vendor = 'Unknown'
        self.module = 'Unknown'

    def get_file(self):
        """
        Try to locate composer,json file.
        1. If '/vendor/' in filePath, return filepath/to/vendor/xxx/xxx/composer.json
        2. Search for composer.json file in each of the folders beginning
            from the deepest path.
        """

        vendorDir = '/vendor/'
        if vendorDir in self.filePath:
            root, modulePath = self.filePath.split(vendorDir)
            self.vendor, self.module, rest = modulePath.split(os.sep, 2)
            composer = os.sep.join([root, 'vendor', self.vendor, self.module, 'composer.json'])
            if os.path.isfile(composer) and os.path.getsize(composer) > 0:
                return composer
        else:
            folders = self.filePath.split(os.sep)
            folders.pop() # remove filename
            folders.append('composer.json')
            while len(folders) > 1:
                composer = os.sep.join(folders)
                print(composer)
                if os.path.isfile(composer) and os.path.getsize(composer) > 0:
                    return composer
                else:
                    del folders[len(folders) - 2] # remove last folder

        return None

    def load(self):
        composer = self.get_file()
        if composer is not None:
            with open(composer) as file:
                self.data = json.loads(file.read())
        else:
            self.data = {
                'name': self.vendor + '/' + self.module,
                'type': 'magento2-module',
                'autoload': {
                    'psr-4': {
                        camelcase(self.vendor) + '\\' + camelcase(self.module): ''
                    }
                }
            }

    def get_name(self):
        return self.get_data('name')

    def get_vendor(self):
        return self.get_name().split('/')[0]

    def get_project(self):
        return self.get_name().split('/')[1]

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
