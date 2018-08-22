import os

from .filters import *

class Project:
    def __init__(self, app):
        self.app = app

    def path(self):
        path = self.app.composer.path().replace('/composer.json', '')
        subdir = self.app.composer.psr4().get(self.app.env.psr4key())
        if subdir:
            path += os.sep + subdir
        return path

    def code(self):
        return self.app.env.psr4key().replace('\\', '_').strip('_')

    def vendor(self):
        psr4key = self.app.env.psr4key()
        if psr4key:
            return kebabcase(psr4key.split('\\')[0])
        else:
            return self.app.composer.vendor()

    def project(self):
        psr4key = self.app.env.psr4key()
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
        app = self.app.composer.type()
        if app is not None:
            knowntypes = {
                'magento2-': 'magento2',
                'magento-': 'magento1'
            }
            for key in knowntypes:
                if key in app:
                    return knowntypes[key]

        # @todo: try to detect by `require` section

        # @todo: detect by `current_syntax` (php, etc)

        # @todo: fallback to default value from config
        return 'magento2'
