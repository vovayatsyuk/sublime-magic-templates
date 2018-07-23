class MagentoVersion:
    def __init__(self, path):
        return

    def isM1(self):
        return not isM2()

    def isM2(self):
        # 1. Check by a composer.json file in module root
        #   If composer.json is missing - M1 and goto step2
        #   If found - detect by type
        #       If type is metapackage - see the require section
        #       If still not sure - give up
        # 2. Check by a composer.json file in Magento root
        #   If can't fine magento root - give up
        return True

class MagentoModule:
    def getPath(self):
        return 'module path'

    def getComposerJson(self, key):
        return 'parsed composer.json or some value if key is recieved'
