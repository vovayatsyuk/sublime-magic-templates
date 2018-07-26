import sublime
import re

from .namespace import getNamespace
from .classname import getClassName
from .composer import Composer

class Variables:
    def __init__(self, filePath):
        self.filePath = filePath
        self.composer = Composer(filePath)

    def extract(self, variables):
        result = {};
        for var in variables:
            result[var] = getattr(self, 'get_' + var)()
        return result

    def get_package(self):
        return self.composer.get_name()

    def get_vendor(self):
        return self.composer.get_vendor()

    def get_project(self):
        return self.composer.get_project()

    def get_psr4(self):
        return list(self.composer.get_psr4().keys())[0]

    def get_namespace(self):
        return getNamespace(self.filePath)

    def get_classname(self):
        return getClassName(self.filePath)
