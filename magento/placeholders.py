import sublime
import re

from .filters import *
from .phpfile import Phpfile
from .composer import Composer

class Placeholders:
    def __init__(self, file_path):
        self.file_path = file_path
        self.composer = Composer(file_path)
        self.phpfile = Phpfile(file_path)

    def extract(self, names):
        result = {};
        for name in names:
            params = name.split('|')
            method = params.pop(0)
            result[name] = getattr(self, 'get_' + method)()
            for string_filter in params:
                result[name] = globals()[string_filter](result[name])
        return result

    def get_package(self):
        return self.composer.get_name()

    def get_vendor(self):
        return self.composer.get_vendor()

    def get_project(self):
        return self.composer.get_project()

    def get_namespace(self):
        return self.phpfile.get_namespace()

    def get_classname(self):
        return self.phpfile.get_classname()
