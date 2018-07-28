import os
import json

class Composer:
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = None

    def get_file(self):
        """
        Locate composer.json file by the following rules:
        1. If 'vendor/' in filePath, return filepath/to/vendor/xxx/xxx/composer.json
        2. If not, search for composer.json file in each of the folders beginning
            from the deepest path.
        """
        vendorDir = '/vendor/'
        if vendorDir in self.filePath:
            root, modulePath = self.filePath.split(vendorDir)
            vendor, module, rest = modulePath.split(os.sep, 2)
            composer = os.sep.join([root, 'vendor', vendor, module, 'composer.json'])
            if os.path.isfile(composer):
                return composer

        return None

    def load(self):
        composer = self.get_file()
        if composer is not None:
            with open(composer) as file:
                contents = file.read()
        else:
            # @todo: build virtual data based on file path
            contents = r"""{
                "name": "hello/wor-ld",
                "description": "N/A",
                "type": "magento2-module",
                "version": "1.0.0",
                "autoload": {
                    "psr-4": {
                        "Hello\\WorLd\\": ""
                    }
                }
            }"""
        self.data = json.loads(contents)

    def get_name(self):
        return self.get_data('name')

    def get_vendor(self):
        return self.get_name().split('/')[0]

    def get_project(self):
        return self.get_name().split('/')[1]

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
