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

    def render_snippet(self, alias=None):
        return self.render(self.guess_template_path(alias))

    def render(self, template_path=None, base_dir=None):
        if template_path is None:
            template_path = self.guess_template_path()
            base_dir = self.base_dir
        elif base_dir is None:
            base_dir = self.base_dir

        if '.txt' not in template_path:
            template_path = template_path + '.txt'

        content = sublime.load_resource(os.sep.join([base_dir, template_path]))
        placeholders = [keys[1] for keys in Formatter().parse(content) if keys[1] is not None]

        return content.format(**Placeholders(self.file_path).extract(placeholders))

    def guess_template_path(self, alias=None):
        app = self.env.get_app()
        if app is None:
            return None

        content = sublime.load_resource(os.sep.join([self.base_dir, app, 'rules.json']))
        rules = json.loads(content, object_pairs_hook=OrderedDict)

        if alias is not None:
            if alias in rules:
                return rules[alias].get('path')
            return None

        path = None
        for alias in rules:
            pattern = rules[alias].get('pattern')
            if pattern is None:
                continue
            r = re.compile(pattern)
            if r.search(self.file_path) is not None:
                path = rules[alias].get('path')
                break

        return path
