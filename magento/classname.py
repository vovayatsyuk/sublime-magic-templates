import os

from .composer import Composer

def getClassName(filePath):
    composer = Composer(filePath)
    path = os.path.splitext(filePath)[0] # remove file extension

    pathParts = []
    codePoolDirectory = 'app' + os.sep + 'code' + os.sep
    moduleType = composer.get_type()

    # Magento 2
    if moduleType is not None and 'magento2' in moduleType:
        pathParts.append(path.split(os.sep)[-1])
    elif codePoolDirectory in filePath:
        pathParts = path.split(codePoolDirectory)[1].split(os.sep)
        pathParts.pop(0) # unset namespace part: local|core|community
        if 'controllers' in pathParts:
            pathParts.remove('controllers')

    return '_'.join(pathParts)
