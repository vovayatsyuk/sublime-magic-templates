import os
import json

from .composer import Composer

def getNamespace(filePath):
    composer = Composer(filePath)
    composerPath = composer.get_file()
    if composerPath is None:
        print('composer.json not found')
        return

    modulePath = composerPath.replace('composer.json', '')
    relativePath = filePath.replace(modulePath, '').split(os.sep)
    del relativePath[-1] # remove file name
    relativePath = os.sep.join(relativePath)
    namespace = relativePath
    psr4 = composer.get_psr4()
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
