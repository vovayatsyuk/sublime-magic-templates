import sys
import json
from unittest import TestCase
from collections import OrderedDict

app_module = sys.modules["sublime-magic-templates.mt.app"]

class TestFile(TestCase):
    def test_path(self):
        files = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php',
            'path/to/vendor/name/module/src/Model/Entity.php',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt'
        }

        for filepath in files:
            app = app_module.App(filepath)
            self.assertEqual(filepath, app.file.path())

    def test_relative_path(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Block/Subfolder/Block.php',
            'path/to/vendor/name/module/src/Model/Entity.php': 'src/Model/Entity.php',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt': 'subfolder/Model/Entity.php.txt'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            app.composer._path = 'path/to/vendor/name/module/composer.json'
            self.assertEqual(mapping[filepath], app.file.relative_path())

    def test_autoload_path(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Block/Subfolder/Block.php',
            'path/to/vendor/name/module/unregistered/Block/Subfolder/Block.php': 'unregistered/Block/Subfolder/Block.php',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Model/Entity.php',
            'path/to/vendor/name/module/subfolder/Model/Entity.php': 'Model/Entity.php'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            app.composer._path = 'path/to/vendor/name/module/composer.json'
            app.composer._data = json.loads(
                """{
                    "autoload": {
                        "psr-4": {
                            "Src\\\\Src\\\\": "src/",
                            "Src2\\\\Src2\\\\": "subfolder/",
                            "Name\\\\Module\\\\": ""
                        }
                    }
                }""",
                object_pairs_hook=OrderedDict
            )
            self.assertEqual(mapping[filepath], app.file.autoload_path())

    def test_basename(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Block',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Entity',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt': 'Entity.php'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.file.basename())

    def test_folder(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Subfolder',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Model',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt': 'Model'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.file.folder())

    def test_parent_folder(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Block',
            'path/to/vendor/name/module/src/Model/Entity.php': 'src',
            'path/to/vendor/name/module/subfolder/Model/Entity.php.txt': 'subfolder'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            self.assertEqual(mapping[filepath], app.file.parent_folder())

    def test_psr4key(self):
        mapping = {
            'path/to/vendor/name/module/Block/Subfolder/Block.php': 'Name\\Module\\',
            'path/to/vendor/name/module/src/Model/Entity.php': 'Src\\Src\\',
            'path/to/vendor/name/module/subfolder/Model/Entity.php': 'Src2\\Src2\\'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            app.composer._path = 'path/to/vendor/name/module/composer.json'
            app.composer._data = json.loads(
                """{
                    "autoload": {
                        "psr-4": {
                            "Src\\\\Src\\\\": "src/",
                            "Src2\\\\Src2\\\\": "subfolder/",
                            "Name\\\\Module\\\\": ""
                        }
                    }
                }""",
                object_pairs_hook=OrderedDict
            )
            self.assertEqual(mapping[filepath], app.file.psr4key())

    def test_psr4dir(self):
        mapping = {
            'path/to/vendor/name/module/src/Model/Entity.php': 'src/',
            'path/to/vendor/name/module/subfolder/Model/Entity.php': 'subfolder/',
            'path/to/vendor/name/module/tests/Model/Entity.php': 'tests/'
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            app.composer._path = 'path/to/vendor/name/module/composer.json'
            app.composer._data = json.loads(
                """{
                    "autoload": {
                        "psr-4": {
                            "Src\\\\Src\\\\": "src/",
                            "Src2\\\\Src2\\\\": "subfolder/"
                        }
                    },
                    "autoload-dev": {
                        "psr-4": {
                            "Name\\\\Module\\\\": "tests/"
                        }
                    }
                }""",
                object_pairs_hook=OrderedDict
            )
            self.assertEqual(mapping[filepath], app.file.psr4dir())
