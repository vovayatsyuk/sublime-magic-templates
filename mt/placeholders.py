import sublime
import re
import os

from string import Formatter
from .filters import *

class Placeholders:
    def __init__(self, app):
        self.app = app
        self.composer = app.composer
        self.phpfile = app.phpfile
        self.env = app.env
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
        return self.composer.name()

    def vendor(self):
        return self.composer.vendor()

    def project(self):
        return self.composer.project()

    def vendor_folder(self):
        return self.composer.vendor_folder()

    def project_folder(self):
        return self.composer.project_folder()

    def psr4key(self):
        return self.env.psr4key()

    def module(self):
        return self.psr4key().replace('\\', '_').strip('_')

    def namespace(self):
        return self.phpfile.namespace()

    def classname(self):
        return self.phpfile.classname()

    def basename(self):
        return self.env.file()

    def folder(self):
        return self.env.folder()

    def ipaddress(self):
        try:
            from IpAddress.ipaddress.IpAddress import IpAddress as IpAddress
        except ImportError:
            return sublime.error_message("Please install IpAddress plugin.")

        return IpAddress.instance().get()
