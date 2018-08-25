import sys
from unittest import TestCase

app_module = sys.modules["sublime-magic-templates.mt.app"]

class TestEnv(TestCase):
    def test_folder(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Subfolder',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Model',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt': 'Model'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.env.folder())

    def test_file(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Block',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Entity',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt': 'Entity.php'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.env.file())

    def test_psr4key(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Name\\Module\\',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Src\\Src\\',
            'path/to/vendor/name/module/subfolder/Model/Entity.php': 'Src2\\Src2\\'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            app.composer._path = 'path/to/vendor/name/module/composer.json'
            app.composer._data = {
                "autoload": {
                    "psr-4": {
                        "Src\\Src\\": "src/",
                        "Src2\\Src2\\": "subfolder/",
                        "Name\\Module\\": ""
                    }
                }
            }
            self.assertEqual(mapping[filepath], app.env.psr4key())
