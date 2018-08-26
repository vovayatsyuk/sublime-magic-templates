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
        module_type = self.composer.type()

        # Magento 2
        if module_type is not None and 'magento2' in module_type:
            path_parts.append(path.split(os.sep)[-1])
        elif appcode_dir in self.filepath:
            path_parts = path.split(appcode_dir)[1].split(os.sep)
            path_parts.pop(0) # unset namespace part: local|core|community
            if 'controllers' in path_parts:
                path_parts.remove('controllers')

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
