import os

from .filters import *

class Project:
    def __init__(self, app):
        self.app = app

    def root(self):
        return self.app.composer.path().replace('/composer.json', '')

    def code(self):
        return self.app.file.psr4key().replace('\\', '_').strip('_')

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
        if self.app.composer.path():
            result = self.guess_type_by_composer()

        if result is None:
            result = 'php'

        return result

    def guess_type_by_composer(self):
        rules = [(
            'type', [
                ('magento2-', 'magento2'),
                ('magento-', 'magento1'),
            ]
        ), (
            'extra', [
                ('magento-root-dir', 'magento1'),
            ]
        ), (
            'vendor', [
                ('magento', 'magento2'),
            ]
        )]

        for key, _rules in rules:
            try:
                compare = getattr(self.app.composer, key)()
            except:
                compare = self.app.composer.data(key)

            if compare is not None:
                for fingerprint, _type in _rules:
                    if fingerprint in compare:
                        return _type

        return None
