import os
import json
import sublime

from .filters import *

class Composer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.vendor = 'Unknown'
        self.module = 'Unknown'

    def get_file(self):
        """
        Try to locate composer,json file.
        1. If '/vendor/' in file_path, return path/to/vendor/xxx/xxx/composer.json
        2. Search for composer.json file in each of the folders beginning
            from the deepest path.
        """

        vendor_dir = '/vendor/'
        if vendor_dir in self.file_path:
            root, module_path = self.file_path.split(vendor_dir)
            self.vendor, self.module, rest = module_path.split(os.sep, 2)
            composer = os.sep.join([root, 'vendor', self.vendor, self.module, 'composer.json'])
            if os.path.isfile(composer) and os.path.getsize(composer) > 0:
                return composer
        else:
            root = sublime.active_window().extract_variables().get('folder')
            min_depth = root.count('/') + 1
            folders = self.file_path.split(os.sep)
            folders.pop() # remove filename
            folders.append('composer.json')
            while len(folders) > min_depth:
                composer = os.sep.join(folders)
                if os.path.isfile(composer) and os.path.getsize(composer) > 0:
                    return composer
                else:
                    del folders[len(folders) - 2] # remove last folder

        print('composer.json not found')
        return None

    def load(self):
        composer = self.get_file()
        if composer is not None:
            with open(composer) as file:
                self.data = json.loads(file.read())
        else:
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
        # @todo: read info from psr4. Just like in get_project
        # @see: https://github.com/magepal/magento2-google-tag-manager/blob/master/composer.json
        return self.get_name().split('/')[0]

    def get_project(self):
        psr4key = self.get_current_psr4key()
        print(psr4key)
        if psr4key:
            parts = psr4key.split('\\')
            if len(parts) > 1:
                return kebabcase(parts[1])

        # Logic below is used, when composer is not found
        project = self.get_project_folder()
        removes = [
            'magento2-',
            'magento-2-',
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

    def get_current_psr4key(self):
        module_path = self.get_file().replace('composer.json', '')
        relative_path = self.file_path.replace(module_path, '')
        psr4 = self.get_psr4()
        if psr4 is None:
            return None
        for key in psr4:
            subfolder = psr4[key].strip('/')
            if subfolder:
                if relative_path.startswith(subfolder):
                    return key
            else:
                return key
        return None

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
