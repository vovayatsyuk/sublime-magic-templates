import os
import json

class Phpfile:
    def __init__(self, app):
        self.app = app
        self.filepath = app.filepath
        self.composer = app.composer

    def classname(self):
        path = os.path.splitext(self.filepath)[0] # remove file extension

        path_parts = []
        appcode_dir = 'app' + os.sep + 'code' + os.sep
        module_type = self.app.project.type()

        # Magento 1
        if self.app.project.type() != 'magento2' and appcode_dir in self.filepath:
            path_parts = path.split(appcode_dir)[1].split(os.sep)
            path_parts.pop(0) # unset namespace part: local|core|community
            if 'controllers' in path_parts:
                path_parts.remove('controllers')
        else:
            path_parts.append(self.app.file.basename())

        return '_'.join(path_parts)

    def namespace(self):
        composer_path = self.composer.path()
        if composer_path is None:
            return

        path_parts = self.app.file.autoload_path().split(os.sep)
        del path_parts[-1] # remove file name

        namespace = self.app.file.psr4key()
        if path_parts:
            namespace += '\\'.join(path_parts)

        return namespace.strip('\\')
