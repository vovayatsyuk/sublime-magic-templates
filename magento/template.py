import sublime
import re

from string import Formatter
from .variables import Variables

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
        variables = [keys[1] for keys in Formatter().parse(content) if keys[1] is not None]

        return content.format(**Variables(self.filePath).extract(variables))

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
            # 'Model/.*\.php': 'Model/Entity.php',
            '.*\.php': 'default.php.txt'
        }

        for pattern in rules:
            r = re.compile(pattern)
            if r.search(self.filePath) is not None:
                template = rules[pattern]
                break

        return template
