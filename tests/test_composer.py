import os
import sys
from unittest import TestCase

app_module = sys.modules["sublime-magic-templates.mt.app"]

class TestComposer(TestCase):
    def test_path(self):
        # 1. composer.json doesn't exist
        filepaths = [
            'path/to/vendor/name/module/Block/Subfolder/Block.php',
            'path/to/vendor/vendor-name/module-name/README.md',
        ];

        for filepath in filepaths:
            app = app_module.App(filepath)
            self.assertEqual(None, app.composer.path())

        # 2. composer.json exists
        mapping = {
            '/fixtures/vendor/v-name/module/Model/Entity.php': '/fixtures/vendor/v-name/module/composer.json',
            '/fixtures/app/code/Name/Module/Model/Entity.php': '/fixtures/app/code/Name/Module/composer.json',
            '/fixtures/app/code/Core/Data.php': '/fixtures/composer.json',
        };

        dirpath = os.path.dirname(os.path.realpath(__file__))
        for filepath in mapping:
            app = app_module.App(dirpath + filepath)
            self.assertEqual(dirpath + mapping[filepath], app.composer.path())

    def test_name(self):
        # 1. composer.json doesn't exist
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'name/module',
            'path/to/vendor/vendor-name/module-name/README.md': 'vendor-name/module-name'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.composer.name())

        # 2. composer.json exists
        mapping = {
            '/fixtures/vendor/v-name/module/Model/Entity.php': 'v-name/module',
            '/fixtures/app/code/Name/Module/Model/Entity.php': 'name/module',
            '/fixtures/app/code/Core/Data.php': 'vendor/project',
        };

        dirpath = os.path.dirname(os.path.realpath(__file__))
        for filepath in mapping:
            app = app_module.App(dirpath + filepath)
            self.assertEqual(mapping[filepath], app.composer.name())

    def test_vendor(self):
        # 1. composer.json doesn't exist
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'name',
            'path/to/vendor/vendor-name/module-name/README.md': 'vendor-name'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.composer.vendor())

        # 2. composer.json exists
        mapping = {
            '/fixtures/vendor/v-name/module/Model/Entity.php': 'v-name',
            '/fixtures/app/code/Name/Module/Model/Entity.php': 'name',
            '/fixtures/app/code/Core/Data.php': 'vendor',
        };

        dirpath = os.path.dirname(os.path.realpath(__file__))
        for filepath in mapping:
            app = app_module.App(dirpath + filepath)
            self.assertEqual(mapping[filepath], app.composer.vendor())

    def test_project(self):
        # 1. composer.json doesn't exist
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'module',
            'path/to/vendor/vendor-name/module-name/README.md': 'module-name'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.composer.project())

        # 2. composer.json exists
        mapping = {
            '/fixtures/vendor/v-name/module/Model/Entity.php': 'module',
            '/fixtures/app/code/Name/Module/Model/Entity.php': 'module',
            '/fixtures/app/code/Core/Data.php': 'project',
        };

        dirpath = os.path.dirname(os.path.realpath(__file__))
        for filepath in mapping:
            app = app_module.App(dirpath + filepath)
            self.assertEqual(mapping[filepath], app.composer.project())

    def test_psr4(self):
        # 1. composer.json doesn't exist
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Name\\Module\\',
            'path/to/vendor/vendor-name/module-name/README.md': 'VendorName\\ModuleName\\'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], next(iter(app.composer.psr4())))

        # 2. composer.json exists
        mapping = {
            '/fixtures/vendor/v-name/module/Model/Entity.php': 'Hello\\World\\',
            '/fixtures/app/code/Name/Module/Model/Entity.php': 'Hello\\World2\\',
            '/fixtures/app/code/Core/Data.php': 'Code\\',
        };

        dirpath = os.path.dirname(os.path.realpath(__file__))
        for filepath in mapping:
            app = app_module.App(dirpath + filepath)
            self.assertEqual(mapping[filepath], next(iter(app.composer.psr4())))

    def test_data(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        app = app_module.App(dirpath + '/fixtures/app/code/Core/Data.php')
        self.assertEqual('Description', app.composer.data('description'))
        self.assertEqual('composer', app.composer.data('repositories.magento.type'))
        self.assertEqual('https://repo.magento.com/', app.composer.data('repositories.magento.url'))
