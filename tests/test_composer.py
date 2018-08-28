import sys
from unittest import TestCase

app_module = sys.modules["sublime-magic-templates.mt.app"]

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
