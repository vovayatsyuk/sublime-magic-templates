import sublime
import re
import os

from string import Formatter
from .filters import *

class Placeholders:
    def __init__(self, app):
        self.app = app
        self.memo = {}

    def extract(self, names):
        result = {};
        for name in names:
            if (name in self.memo):
                result[name] = self.memo[name]
            else:
                clean_name = name;
                # placheolder inside placeholder. Eg: {filename|remove {vendor|lower}}
                # @todo: wrap into loop
                if '{' in name:
                    placeholders = [keys[1] for keys in Formatter().parse(name) if keys[1] is not None]
                    clean_name = name.format(**Placeholders(self.app).extract(placeholders))

                params = clean_name.split('|')
                method = params.pop(0)
                result[name] = getattr(self, method)()
                for string_filter in params:
                    args = [result[name]]
                    if ' ' in string_filter:
                        string_filter, args = string_filter.split(' ', 2)
                        args = args.split(',')
                        args.insert(0, result[name])
                    result[name] = globals()[string_filter](*args)

                self.memo[name] = result[name]

        return result

    def package(self):
        return self.app.composer.name()

    def vendor_folder(self):
        return self.app.composer.vendor()

    def project_folder(self):
        return self.app.composer.project()

    def vendor(self):
        return self.app.project.vendor()

    def project(self):
        return self.app.project.project()

    def module(self):
        return self.app.project.code()

    def psr4key(self):
        return self.app.env.psr4key()

    def basename(self):
        return self.app.env.file()

    def folder(self):
        return self.app.env.folder()

    def namespace(self):
        return self.app.phpfile.namespace()

    def classname(self):
        return self.app.phpfile.classname()

    def ipaddress(self):
        try:
            from IpAddress.ipaddress.IpAddress import IpAddress as IpAddress
        except ImportError:
            return sublime.error_message("Please install IpAddress plugin.")

        return IpAddress.instance().get()
