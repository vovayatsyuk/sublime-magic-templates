import sublime
import re
import json

class Composer:
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = None

    def get_file(self):
        return None

    def load(self):
        if self.get_file() is not None:
            with open(self.get_file()) as file:
                contents = file.read()
        else:
            # @todo: build virtual data based on file path
            contents = r"""{
                "name": "hello/world",
                "description": "N/A",
                "type": "magento2-module",
                "version": "1.0.0",
                "autoload": {
                    "psr-4": {
                        "Hello\\World\\": ""
                    }
                }
            }"""
        self.data = json.loads(contents.replace("\\", "\\\\"))

    def get_name(self):
        return self.get_data('name')

    def get_vendor(self):
        return self.get_name().split('/')[0]

    def get_project(self):
        return self.get_name().split('/')[1]

    def get_psr4(self):
        return self.get_data('autoload.psr-4')
        # return r'Hello\\\\World\\\\' # psr-4 from composer.json or folder names in CamelCase joined with '\\'

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
