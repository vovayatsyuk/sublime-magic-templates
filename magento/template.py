import sublime
import json
import re
import os

from string import Formatter
from collections import OrderedDict
from .env import Env
from .placeholders import Placeholders

class Template:
    def __init__(self, file_path):
        self.base_dir = 'Packages/sublime-magento/magento/templates'
        self.file_path = file_path
        self.env = Env(file_path)

    def render(self, template_path=None):
        if template_path is None:
            template_path = self.guess_template_path()

        content = sublime.load_resource(os.sep.join([self.base_dir, template_path]))
        placeholders = [keys[1] for keys in Formatter().parse(content) if keys[1] is not None]

        return content.format(**Placeholders(self.file_path).extract(placeholders))

    def guess_template_path(self):
        app = self.env.get_app()
        if app is None:
            return None

        path = None
        content = sublime.load_resource(os.sep.join([self.base_dir, app, 'rules.json']))
        rules = json.loads(content, object_pairs_hook = OrderedDict)

        for pattern in rules:
            r = re.compile(pattern)
            if r.search(self.file_path) is not None:
                path = rules[pattern]
                break

        if path is not None:
            path = app + os.sep + path

        return path
