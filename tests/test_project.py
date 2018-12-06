import os
import sys
import sublime
from unittest import TestCase

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from mt.app import App

class TestProject(TestCase):
    def test_root(self):
        mapping = {
            'path/to/vendor/name/module/composer.json': 'path/to/vendor/name/module'
        };

        for filepath in mapping:
            app = App(filepath)
            app.composer._path = filepath
            self.assertEqual(mapping[filepath], app.project.root())

    def test_code(self):
        mapping = {
            'Name\\Module\\': 'Name_Module',
            'VendorName\\ModuleName\\': 'VendorName_ModuleName'
        };

        for psr4key in mapping:
            app = App('dummy')
            app.file._psr4key = psr4key
            self.assertEqual(mapping[psr4key], app.project.code())

    def test_vendor_by_psr4key(self):
        mapping = {
            'Name\\Module\\': 'name',
            'VendorName\\ModuleName\\': 'vendor-name'
        };

        for psr4key in mapping:
            app = App('dummy')
            app.file._psr4key = psr4key
            self.assertEqual(mapping[psr4key], app.project.vendor())

    def test_vendor_by_package_name(self):
        mapping = {
            'vendor-name/module-hello-world': 'vendor-name',
            'swissup/magento2-hello-world': 'swissup',
        };

        for package in mapping:
            app = App('dummy')
            app.composer._data = {
                'name': package
            }
            self.assertEqual(mapping[package], app.project.vendor())

    def test_project_by_psr4key(self):
        # with defined psr4keys
        mapping = {
            'Name\\Module\\': 'module',
            'VendorName\\ModuleName\\': 'module-name'
        };

        for psr4key in mapping:
            app = App('dummy')
            app.file._psr4key = psr4key
            self.assertEqual(mapping[psr4key], app.project.project())

    def test_project_by_package_name(self):
        # without defined psr4keys
        mapping = {
            'vendor/module-hello-world': 'hello-world',
            'swissup/magento2-hello-world': 'hello-world',
            'swissup/magento-2-hello-world': 'hello-world',
            'swissup/magento1-hello-world': 'hello-world',
            'swissup/magento-hello-world': 'hello-world',
            'swissup/hello-world-extension': 'hello-world',
            'swissup/hello-world-magento-2': 'hello-world',
        };

        for package in mapping:
            app = App('dummy')
            app.composer._data = {
                'name': package
            }
            self.assertEqual(mapping[package], app.project.project())

    def test_guess_type_by_contents(self):
        mapping = {
            'extends Magento': 'magento2',
            'extends Mage_': 'magento1',
            '$a = Mage::': 'magento1'
        };
        for contents in mapping:
            app = App('dummy')

            self.view = sublime.active_window().new_file()

            self.view.run_command('insert', {'characters': contents})

            _type = app.project.guess_type_by_contents()

            self.view.window().focus_view(self.view)
            self.view.set_scratch(True)
            self.view.window().run_command('close_file')

            self.assertEqual(mapping[contents], _type)

    def test_guess_type_by_composer_by_type(self):
        mapping = {
            'magento2-module': 'magento2',
            'magento-module': 'magento1',
            None: None
        };
        for project_type in mapping:
            app = App('dummy')
            app.composer._data = {
                'type': project_type
            }
            self.assertEqual(mapping[project_type], app.project.guess_type_by_composer())

    def test_guess_type_by_composer_by_extra(self):
        app = App('dummy')
        app.composer._data = {
            'extra': {
                'magento-root-dir': '.'
            }
        }
        self.assertEqual('magento1', app.project.guess_type_by_composer())

    def test_guess_type_by_composer_by_vendor(self):
        app = App('dummy')
        app.composer._data = {
            'name': 'magento/magento2ce'
        }
        self.assertEqual('magento2', app.project.guess_type_by_composer())
