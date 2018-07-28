import os
import json

from .composer import Composer

def getNamespace(filePath):
    pathParts = []
    vendorDirectory = 'vendor' + os.sep
    if not vendorDirectory in filePath:
        print(vendorDirectory + ' not found in ' + filePath)
        return

    pathParts = filePath.split(vendorDirectory)[1].split(os.sep)
    del pathParts[:2] # remove vendor and module folders
    del pathParts[-1] # remove file name

    currentPath = os.sep.join(pathParts)
    psr4 = Composer(filePath).get_psr4()
    for key in psr4:
        subfolder = psr4[key].strip('/')

        if subfolder:
            if currentPath.startswith(subfolder):
                currentPath = currentPath[len(subfolder):].lstrip(os.sep)
            else:
                continue

        currentPath = key.replace('\\', os.sep) + currentPath
        currentPath = currentPath.strip(os.sep)
        break

    pathParts = currentPath.split(os.sep);

    return '\\'.join(pathParts)
