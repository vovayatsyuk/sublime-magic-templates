import os
import sys
from unittest import TestCase

app_module = sys.modules["sublime-magic-templates.mt.app"]

class TestComposer(TestCase):
    def test_path(self):
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
        mapping = {
            '/fixtures/vendor/v-name/module/Model/Entity.php': 'v-name/module',
            '/fixtures/app/code/Name/Module/Model/Entity.php': 'name/module',
            '/fixtures/app/code/Core/Data.php': 'vendor/project',
        };

        dirpath = os.path.dirname(os.path.realpath(__file__))
        for filepath in mapping:
            app = app_module.App(dirpath + filepath)
            self.assertEqual(mapping[filepath], app.composer.name())

class TestComposerNotExists(TestCase):
    def test_path(self):
        filepaths = [
            'path/to/vendor/name/module/Block/Subfolder/Block.php',
            'path/to/vendor/vendor-name/module-name/README.md',
        ];

        for filepath in filepaths:
            app = app_module.App(filepath)
            self.assertEqual(None, app.composer.path())

    def test_name(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'name/module',
            'path/to/vendor/vendor-name/module-name/README.md': 'vendor-name/module-name'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.composer.name())

    def test_vendor(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'name',
            'path/to/vendor/vendor-name/module-name/README.md': 'vendor-name'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.composer.vendor())

    def test_project(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'module',
            'path/to/vendor/vendor-name/module-name/README.md': 'module-name'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.composer.project())

    def test_psr4(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Name\\Module\\',
            'path/to/vendor/vendor-name/module-name/README.md': 'VendorName\\ModuleName\\'
        };

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], next(iter(app.composer.psr4())))
