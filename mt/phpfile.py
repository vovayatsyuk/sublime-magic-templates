import os
import json

class Phpfile:
    def __init__(self, app):
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

        module_path = composer_path.replace('composer.json', '')
        relative_path = self.filepath.replace(module_path, '').split(os.sep)
        del relative_path[-1] # remove file name
        relative_path = os.sep.join(relative_path)
        namespace = relative_path

        psr4 = self.composer.psr4()
        if psr4 is None:
            return namespace.replace(os.sep, '\\')

        for key in psr4:
            subfolder = psr4[key].strip('/')
            if subfolder:
                if relative_path.startswith(subfolder):
                    namespace = relative_path[len(subfolder):].lstrip(os.sep)
                else:
                    continue

            namespace = key.replace('\\', os.sep) + namespace
            namespace = namespace.strip(os.sep)
            break

        return namespace.replace(os.sep, '\\')
