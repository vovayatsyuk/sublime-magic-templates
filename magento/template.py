import sublime
import re

from string import Formatter
from .placeholders import Placeholders

class Template:
    def __init__(self, file_path):
        self.file_path = file_path

    def _get_base_path(self):
        return 'Packages/sublime-magento/magento/templates/m2/'

    def render(self):
        template = self._match()
        if template is None:
            return '';

        content = sublime.load_resource(self._get_base_path() + template)
        placeholders = [keys[1] for keys in Formatter().parse(content) if keys[1] is not None]

        return content.format(**Placeholders(self.file_path).extract(placeholders))

    def _match(self):
        if self.file_path is None:
            return None

        rules = [
            ('composer\.json', 'composer.json.txt'),
            # ('Model/.*Repository\.php', 'Model/EntityRepository.php'),
            # ('Model/.*/Source/.*', 'Model/Config/Source.php'),
            # ('Model/.*/DataProvider\.php', 'Model/Source/Options.php'),
            # ('Model/ResourceModel/*/Grid/Collection.php', 'Model/Source/Options.php'),
            # ('Model/ResourceModel/*/Collection.php', 'Model/Source/Options.php'),
            # ('Model/ResourceModel/.*\.php', 'Model/ResourceModel/Entity.php'),
            # ('Model/.*\.php', 'Model/Entity.php'),
            ('Helper/.*\.php', 'Helper/Data.php.txt'),
            ('.*\.php', 'default.php.txt')
        ]

        for pattern, path in rules:
            r = re.compile(pattern)
            if r.search(self.file_path) is not None:
                return path

        return None
