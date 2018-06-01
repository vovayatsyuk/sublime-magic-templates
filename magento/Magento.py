import sublime
import re
import os
import json

class MagentoVersion:
    def __init__(self, path):
        return

    def isM1(self):
        return not isM2()

    def isM2(self):
        # 1. Check by a composer.json file in module root
        #   If composer.json is missing - M1
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

class PhpFile:
    def __init__(self, path):
        return

    def getNamespace(self):
        return ''

    def getClassName(self):
        return ''

    def getTemplate(self):
        return 'path to template file'

    def debug(self, text):
        print('[MagentoSublime] ' + text)

class File:
    def __init__(self, path):
        self.path = path;

    def getTemplate(self):
        return Template('composer')

class Template:
    def __init__(self, filePath):
        self.filePath = filePath
        self.vars = TemplateVariables(filePath)

    def render(self):
        template = sublime.load_resource(
            'Packages/magento-sublime/' + self.__match(self.filePath)
        )
        return template.format(**self.vars.extract(template))

    def __match(self, filePath):
        return 'templates/m2/composer.txt'

class TemplateVariables:
    def __init__(self, filePath):
        self.filePath = filePath

    def extract(self, template):
        return {
            'package': 'hello/world',       # name from composer.json or folder names joined with '/'
            'vendor': 'hello',              # --//--
            'module': 'world',              # --//--
            'psr-4': r'Hello\\\\World\\\\'  # psr-4 from composer.json or folder names in CamelCase joined with '\\'
        }

class ClassNameDetector(object):
    def __init__(self, path):
        path = os.path.splitext(path)[0] # remove file extension

        self.pathParts = []
        self.codePoolDirectory = 'app' + os.sep + 'code' + os.sep

        if not self.codePoolDirectory in path:
            # Magento 2
            self.pathParts.append(path.split(os.sep)[-1])
            return

        self.pathParts = path.split(self.codePoolDirectory)[1].split(os.sep)
        self.pathParts.pop(0) # unset namespace part: local|core|community

        if 'controllers' in self.pathParts:
            self.pathParts.remove('controllers')

    def getClassName(self):
        return '_'.join(self.pathParts)

    def debug(self, text):
        print('[Magento ClassNameDetector] ' + text)

class NamespaceDetector(object):
    def __init__(self, path):
        self.pathParts = []
        self.vendorDirectory = 'vendor' + os.sep
        if not self.vendorDirectory in path:
            self.debug(self.vendorDirectory + ' not found in ' + path)
            return

        self.pathParts = path.split(self.vendorDirectory)[1].split(os.sep)
        del self.pathParts[:2] # remove vendor and module folders
        del self.pathParts[-1] # remove file name

        # get psr-4 settings
        modulePath = path.split(os.sep.join(self.pathParts))[0]
        with open(modulePath + 'composer.json') as composer:
            data = json.load(composer)

        currentPath = os.sep.join(self.pathParts)
        for key in data['autoload']['psr-4']:
            subfolder = data['autoload']['psr-4'][key]

            if subfolder:
                if currentPath.startswith(subfolder):
                    currentPath = currentPath[len(subfolder):]
                else:
                    continue

            currentPath = key.replace('\\', os.sep) + currentPath
            break

        self.pathParts = currentPath.split(os.sep);

    def getNamespace(self):
        return '\\'.join(self.pathParts)

    def debug(self, text):
        print('[Magento NamespaceDetector] ' + text)
