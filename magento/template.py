import sublime
import re

from string import Formatter

class Template:
    def __init__(self, filePath):
        self.filePath = filePath

    def __getBasePath(self):
        return 'Packages/sublime-magento/magento/templates/m2/'

    def render(self):
        template = self.__match()
        if template is None:
            return '';

        content = sublime.load_resource(self.__getBasePath() + template)

        return content.format(**self.__extractVariables(content))

    def __match(self):
        template = None

        if self.filePath is None:
            return template

        rules = {
            'composer\.json': 'composer.json.txt',
            # 'Model/.*Repository\.php': 'Model/EntityRepository.php',
            # 'Model/.*/Source/.*': 'Model/Config/Source.php',
            # 'Model/.*/DataProvider\.php': 'Model/Source/Options.php',
            # 'Model/ResourceModel/*/Grid/Collection.php': 'Model/Source/Options.php',
            # 'Model/ResourceModel/*/Collection.php': 'Model/Source/Options.php',
            # 'Model/ResourceModel/.*\.php': 'Model/ResourceModel/Entity.php',
            # 'Model/.*\.php': 'Model/Entity.php'
        }

        for pattern in rules:
            r = re.compile(pattern)
            if r.search(self.filePath) is not None:
                template = rules[pattern]
                break

        return template

    def __extractVariables(self, template):
        # 1. parse template to get all required variables
        keys = [keys[1] for keys in Formatter().parse(template) if keys[1] is not None]

        for key in keys:
            print(key);

        # 2. return these variables
        return {
            'package': 'hello/world',           # name from composer.json or folder names joined with '/'
            'vendor' : 'hello',                 # --//--
            'project': 'world',                 # --//--
            'psr-4'  : r'Hello\\\\World\\\\'    # psr-4 from composer.json or folder names in CamelCase joined with '\\'
        }
