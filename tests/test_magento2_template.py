import sys
from unittest import TestCase

app_module = sys.modules["sublime-magic-templates.mt.app"]

class TestMagento2Template(TestCase):
    def test_guess_template_path(self):
        mapping = {
            "vendor/module/Block/Subfolder/Block.php": "magento2/files/Block/Block.php",
            "vendor/module/Controller/Adminhtml/Index.php": "magento2/files/Controller/Adminhtml/Entity/Index.php",
            "vendor/module/Controller/Adminhtml/MassStatus.php": "magento2/files/Controller/Adminhtml/Entity/MassStatus.php",
            "vendor/module/Ui/DataProvider/Entity/Form/DataProvider.php": "magento2/files/Ui/DataProvider/Form/EntityProvider.php",
            "vendor/module/Ui/DataProvider/Form/DataProvider.php": "magento2/files/Ui/DataProvider/Form/EntityProvider.php",
            "vendor/module/Ui/DataProvider/Entity/DataProvider.php": "magento2/files/Ui/DataProvider/EntityProvider.php",
            "vendor/module/Ui/DataProvider/DataProvider.php": "magento2/files/Ui/DataProvider/EntityProvider.php"
        }

        for filepath in mapping:
            app = app_module.App(filepath)
            app.composer.path = "vendor/module/composer.json"
            self.assertEqual(mapping[filepath], app.template.guess_template_path())
