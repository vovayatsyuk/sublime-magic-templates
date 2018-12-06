import os
import sys
from unittest import TestCase

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from mt.app import App

class TestMagento2Template(TestCase):
    def test_guess_template_path(self):
        mapping = {
            "vendor/module/Block/Subfolder/Block.php": "magento2/files/Block/Block.php",

            "vendor/module/Controller/Adminhtml/Index.php": "magento2/files/Controller/Adminhtml/Entity/Index.php",
            "vendor/module/Controller/Adminhtml/NewAction.php": "magento2/files/Controller/Adminhtml/Entity/NewAction.php",
            "vendor/module/Controller/Adminhtml/Edit.php": "magento2/files/Controller/Adminhtml/Entity/Edit.php",
            "vendor/module/Controller/Adminhtml/Save.php": "magento2/files/Controller/Adminhtml/Entity/Save.php",
            "vendor/module/Controller/Adminhtml/MassDelete.php": "magento2/files/Controller/Adminhtml/Entity/MassDelete.php",
            "vendor/module/Controller/Adminhtml/MassStatus.php": "magento2/files/Controller/Adminhtml/Entity/MassStatus.php",
            "vendor/module/Controller/Adminhtml/MassDisable.php": "magento2/files/Controller/Adminhtml/Entity/MassStatus.php",
            "vendor/module/Controller/Adminhtml/Delete.php": "magento2/files/Controller/Adminhtml/Entity/Delete.php",
            "vendor/module/Controller/Adminhtml/Validate.php": "magento2/files/Controller/Adminhtml/Entity/Validate.php",

            "vendor/module/Controller/Name/Index.php": "magento2/files/Controller/Entity/Index.php",
            "vendor/module/Controller/Name/Save.php": "magento2/files/Controller/Entity/Save.php",
            "vendor/module/Controller/Name/Post.php": "magento2/files/Controller/Entity/Save.php",

            "vendor/module/etc/adminhtml/di.xml": "magento2/files/etc/adminhtml/di.xml",
            "vendor/module/etc/adminhtml/events.xml": "magento2/files/etc/adminhtml/events.xml",
            "vendor/module/etc/adminhtml/menu.xml": "magento2/files/etc/adminhtml/menu.xml",
            "vendor/module/etc/adminhtml/routes.xml": "magento2/files/etc/adminhtml/routes.xml",
            "vendor/module/etc/adminhtml/system.xml": "magento2/files/etc/adminhtml/system.xml",
            "vendor/module/etc/frontend/di.xml": "magento2/files/etc/frontend/di.xml",
            "vendor/module/etc/frontend/events.xml": "magento2/files/etc/frontend/events.xml",
            "vendor/module/etc/frontend/page_types.xml": "magento2/files/etc/frontend/page_types.xml",
            "vendor/module/etc/frontend/routes.xml": "magento2/files/etc/frontend/routes.xml",
            "vendor/module/etc/frontend/sections.xml": "magento2/files/etc/frontend/sections.xml",
            "vendor/module/etc/acl.xml": "magento2/files/etc/acl.xml",
            "vendor/module/etc/config.xml": "magento2/files/etc/config.xml",
            "vendor/module/etc/di.xml": "magento2/files/etc/di.xml",
            "vendor/module/etc/events.xml": "magento2/files/etc/events.xml",
            "vendor/module/etc/module.xml": "magento2/files/etc/module.xml",
            "vendor/module/etc/widget.xml": "magento2/files/etc/widget.xml",

            "vendor/module/Helper/Data.php": "magento2/files/Helper/Data.php",
            "vendor/module/Helper/Subfolder/Name.php": "magento2/files/Helper/Data.php",

            "vendor/module/Model/Name.php": "magento2/files/Model/Entity.php",
            "vendor/module/Model/NameRepository.php": "magento2/files/Model/EntityRepository.php",
            "vendor/module/Model/Source/Name.php": "magento2/files/Model/Config/Source/Entity.php",
            "vendor/module/Model/ResourceModel/Name.php": "magento2/files/Model/ResourceModel/Entity.php",
            "vendor/module/Model/ResourceModel/Name/Collection.php": "magento2/files/Model/ResourceModel/Entity/Collection.php",
            "vendor/module/Model/ResourceModel/Name/Grid/Collection.php": "magento2/files/Model/ResourceModel/Entity/Grid/Collection.php",

            "vendor/module/Observer/ClassName.php": "magento2/files/Observer/Default.php",
            "vendor/module/Observer/Subfolder/ClassName.php": "magento2/files/Observer/Default.php",

            "vendor/module/Plugin/Name.php": "magento2/files/Plugin/Default.php",

            "vendor/module/Setup/UpgradeSchema.php": "magento2/files/Setup/UpgradeSchema.php",

            "vendor/module/Ui/DataProvider/EntityProvider.php": "magento2/files/Ui/DataProvider/EntityProvider.php",
            "vendor/module/Ui/DataProvider/Form/EntityProvider.php": "magento2/files/Ui/DataProvider/Form/EntityProvider.php",
            "vendor/module/Ui/DataProvider/Name/Form/EntityDataProvider.php": "magento2/files/Ui/DataProvider/Form/EntityProvider.php",
            "vendor/module/Ui/DataProvider/Name/DataProvider.php": "magento2/files/Ui/DataProvider/EntityProvider.php",
            "vendor/module/Ui/Component/Listing/Columns/SomeActions.php": "magento2/files/Ui/Component/Listing/Columns/Actions.php",
            "vendor/module/Ui/Component/Listing/Columns/FieldRenderer.php": "magento2/files/Ui/Component/Listing/Columns/Default.php",
            "vendor/module/Ui/Component/Listing/Column/FieldRenderer.php": "magento2/files/Ui/Component/Listing/Columns/Default.php",

            "vendor/module/view/adminhtml/layout/vendor_module_index.xml": "magento2/files/view/adminhtml/layout/index.xml",
            "vendor/module/view/adminhtml/layout/vendor_module_edit.xml": "magento2/files/view/adminhtml/layout/edit.xml",
            "vendor/module/view/adminhtml/layout/vendor_module_new.xml": "magento2/files/view/adminhtml/layout/new.xml",
            "vendor/module/view/adminhtml/ui_component/module_entity_listing.xml": "magento2/files/view/adminhtml/ui_component/listing.xml",
            "vendor/module/view/adminhtml/ui_component/module_entity_list.xml": "magento2/files/view/adminhtml/ui_component/listing.xml",
            "vendor/module/view/adminhtml/ui_component/module_entity_form.xml": "magento2/files/view/adminhtml/ui_component/form.xml",
            "vendor/module/view/adminhtml/ui_component/module_entity_new.xml": "magento2/files/view/adminhtml/ui_component/form.xml",
            "vendor/module/view/adminhtml/ui_component/module_entity_edit.xml": "magento2/files/view/adminhtml/ui_component/form.xml",
            "vendor/module/view/frontend/layout/default.xml": "magento2/files/view/base/layout/layout.xml",
            "vendor/module/view/base/layout/default.xml": "magento2/files/view/base/layout/layout.xml",
            "vendor/module/view/frontend/requirejs-config.js": "magento2/files/view/base/requirejs-config.js",
            "vendor/module/view/frontend/web/js/mixin/action-mixin.js": "magento2/files/view/base/web/js/mixin/action-mixin.js",
            "vendor/module/view/frontend/web/js/action-mixin.js": "magento2/files/view/base/web/js/mixin/action-mixin.js",
            "vendor/module/view/frontend/web/js/mixin/name.js": "magento2/files/view/base/web/js/mixin/model-mixin.js",
            "vendor/module/view/frontend/web/js/action/name.js": "magento2/files/view/base/web/js/action.js",
            "vendor/module/view/frontend/web/js/model/name.js": "magento2/files/view/base/web/js/model.js",
            "vendor/module/view/frontend/web/js/view/name.js": "magento2/files/view/base/web/js/view.js",
            "vendor/module/view/frontend/web/js/name.js": "magento2/files/view/base/web/js/default.js",

            "vendor/module/composer.json": "magento2/files/composer.json",
            "vendor/module/README.md": "magento2/files/README.md",
            "vendor/module/registration.php": "magento2/files/registration.php"
        }

        for filepath in mapping:
            app = App(filepath)
            app.composer._path = "vendor/module/composer.json"
            app.composer._data = {
                "type": "magento2-module"
            }
            self.assertEqual(mapping[filepath], app.template.guess_template_path())
