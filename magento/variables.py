import sublime
import re

class Variables:
    def __init__(self, filePath):
        self.filePath = filePath

    def extract(self, variables):
        result = {};

        for var in variables:
            result[var] = getattr(self, 'get_' + var)()

        return result

    def get_package(self):
        return self.get_vendor() + '/' + self.get_project()

    def get_vendor(self):
        return 'hello'  # name from composer.json or folder names

    def get_project(self):
        return 'world' # name from composer.json or folder names

    def get_psr4(self):
        return r'Hello\\\\World\\\\' # psr-4 from composer.json or folder names in CamelCase joined with '\\'
