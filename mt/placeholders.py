import sublime
import re
import os

from string import Formatter
from .filters import *

class Placeholders:
    def __init__(self, app):
        self.app = app
        self.file_path = app.filepath
        self.composer = app.composer
        self.phpfile = app.phpfile

    def extract(self, names):
        result = {};
        for name in names:
            clean_name = name;
            # placheolder inside placeholder. Eg: {filename|remove {vendor|lower}}
            # @todo: wrap into loop
            if '{' in name:
                placeholders = [keys[1] for keys in Formatter().parse(name) if keys[1] is not None]
                clean_name = name.format(**Placeholders(self.app).extract(placeholders))

            params = clean_name.split('|')
            method = params.pop(0)
            result[name] = getattr(self, 'get_' + method)()
            for string_filter in params:
                args = [result[name]]
                if ' ' in string_filter:
                    string_filter, args = string_filter.split(' ', 2)
                    args = args.split(',')
                    args.insert(0, result[name])
                result[name] = globals()[string_filter](*args)
        return result

    def get_package(self):
        return self.composer.get_name()

    def get_vendor(self):
        return self.composer.get_vendor()

    def get_project(self):
        return self.composer.get_project()

    def get_vendor_folder(self):
        return self.composer.get_vendor_folder()

    def get_project_folder(self):
        return self.composer.get_project_folder()

    def get_psr4key(self):
        return self.composer.get_current_psr4key()

    def get_module(self):
        return self.composer.get_current_psr4key().replace('\\', '_').strip('_')

    def get_namespace(self):
        return self.phpfile.get_namespace()

    def get_classname(self):
        return self.phpfile.get_classname()

    def get_basename(self):
        return os.path.splitext(os.path.basename(self.file_path))[0]

    def get_folder(self):
        return os.path.basename(os.path.dirname(self.file_path))

    def get_ipaddress(self):
        try:
            from IpAddress.ipaddress.IpAddress import IpAddress as IpAddress
        except ImportError:
            return sublime.error_message("Please install IpAddress plugin.")

        return IpAddress.instance().get()
