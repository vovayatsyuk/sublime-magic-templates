import sublime
import json
import re
import os

from string import Formatter
from collections import OrderedDict
from .app import App
from .placeholders import Placeholders

class Template:
    def __init__(self, file_path):
        self.file_path = file_path
        self.app = App(file_path)

    def render(self):
        template = self._match()
        if template is None:
            return '';

        content = sublime.load_resource(os.sep.join([
            'Packages/sublime-magento/magento/templates',
            self.app.get_type(),
            template
        ]))
        placeholders = [keys[1] for keys in Formatter().parse(content) if keys[1] is not None]

        return content.format(**Placeholders(self.file_path).extract(placeholders))

    def _match(self):
        if self.file_path is None:
            return None

        content = sublime.load_resource(os.sep.join([
            'Packages/sublime-magento/magento/templates',
            self.app.get_type(),
            'rules.json'
        ]))
        rules = json.loads(content, object_pairs_hook = OrderedDict)

        for pattern in rules:
            r = re.compile(pattern)
            if r.search(self.file_path) is not None:
                return rules[pattern]

        return None
