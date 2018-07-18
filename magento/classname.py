import os

def getClassName(filePath):
    path = os.path.splitext(filePath)[0] # remove file extension

    pathParts = []
    codePoolDirectory = 'app' + os.sep + 'code' + os.sep

    # Magento 2
    if not codePoolDirectory in path:
        pathParts.append(path.split(os.sep)[-1])
    else:
        pathParts = path.split(codePoolDirectory)[1].split(os.sep)
        pathParts.pop(0) # unset namespace part: local|core|community

        if 'controllers' in pathParts:
            pathParts.remove('controllers')

    return '_'.join(pathParts)
