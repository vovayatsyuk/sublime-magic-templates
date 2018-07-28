import sublime
import re

from .filters import *
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
            params = var.split('|')
            method = params.pop(0)
            result[var] = getattr(self, 'get_' + method)()
            for string_filter in params:
                result[var] = globals()[string_filter](result[var])
        return result

    def get_package(self):
        return self.composer.get_name()

    def get_vendor(self):
        return self.composer.get_vendor()

    def get_project(self):
        return self.composer.get_project()

    def get_namespace(self):
        return getNamespace(self.filePath)

    def get_classname(self):
        return getClassName(self.filePath)
