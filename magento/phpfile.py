import os
import json

from .composer import Composer

class Phpfile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.composer = None

    def get_composer(self):
        if self.composer is None:
            self.composer = Composer(self.file_path)
        return self.composer

    def get_classname(self):
        path = os.path.splitext(self.file_path)[0] # remove file extension

        pathParts = []
        codePoolDirectory = 'app' + os.sep + 'code' + os.sep
        moduleType = self.get_composer().get_type()

        # Magento 2
        if moduleType is not None and 'magento2' in moduleType:
            pathParts.append(path.split(os.sep)[-1])
        elif codePoolDirectory in self.file_path:
            pathParts = path.split(codePoolDirectory)[1].split(os.sep)
            pathParts.pop(0) # unset namespace part: local|core|community
            if 'controllers' in pathParts:
                pathParts.remove('controllers')

        return '_'.join(pathParts)

    def get_namespace(self):
        composer = self.get_composer()
        composerPath = composer.get_file()
        if composerPath is None:
            print('composer.json not found')
            return

        modulePath = composerPath.replace('composer.json', '')
        relativePath = self.file_path.replace(modulePath, '').split(os.sep)
        del relativePath[-1] # remove file name
        relativePath = os.sep.join(relativePath)
        namespace = relativePath

        psr4 = composer.get_psr4()
        if psr4 is None:
            return namespace.replace(os.sep, '\\')

        for key in psr4:
            subfolder = psr4[key].strip('/')
            if subfolder:
                if relativePath.startswith(subfolder):
                    namespace = relativePath[len(subfolder):].lstrip(os.sep)
                else:
                    continue

            namespace = key.replace('\\', os.sep) + namespace
            namespace = namespace.strip(os.sep)
            break

        return namespace.replace(os.sep, '\\')
