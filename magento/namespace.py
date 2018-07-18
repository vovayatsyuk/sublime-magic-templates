import os
import json

def getNamespace(filePath):
    pathParts = []
    vendorDirectory = 'vendor' + os.sep
    if not vendorDirectory in filePath:
        print(vendorDirectory + ' not found in ' + filePath)
        return

    pathParts = filePath.split(vendorDirectory)[1].split(os.sep)
    del pathParts[:2] # remove vendor and module folders
    del pathParts[-1] # remove file name

    # get psr-4 settings
    modulePath = filePath.split(os.sep.join(pathParts))[0]
    with open(modulePath + 'composer.json') as composer:
        data = json.load(composer)

    currentPath = os.sep.join(pathParts)
    for key in data['autoload']['psr-4']:
        subfolder = data['autoload']['psr-4'][key].strip('/')

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
