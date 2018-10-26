import sublime
import json
import re
import os

from .utils import load_resource
from string import Formatter
from collections import OrderedDict
from .placeholders import Placeholders

class Template:
    def __init__(self, app):
        self.base_dir = 'Packages/sublime-magic-templates/templates'
        self.app = app
        self.filepath = app.filepath

    def render_snippet(self, alias, base_dir=None):
        if self.filepath is None:
            return None

        return self.render(self.guess_template_path(alias), base_dir)

    def render(self, template_path=None, base_dir=None):
        if self.filepath is None:
            return None

        if template_path is None:
            template_path = self.guess_template_path()
            base_dir = self.base_dir
        elif base_dir is None:
            base_dir = self.base_dir

        if template_path is None:
            return None

        if '.txt' not in template_path:
            template_path = template_path + '.txt'

        content = load_resource(os.sep.join([base_dir, template_path]))
        if content is None:
            return None

        placeholders = [keys[1] for keys in Formatter().parse(content) if keys[1] is not None]

        return content.format(**Placeholders(self.app).extract(placeholders))

    def guess_template_path(self, alias=None):
        project_type = self.app.project.type()
        if project_type is None or self.app.composer.path() is None:
            return None

        rules = load_resource(os.sep.join([self.base_dir, project_type, 'files.json']), True)
        if rules is None:
            return None

        if alias is not None:
            if alias in rules.get('snippets'):
                return rules.get('snippets').get(alias).get('path')
            return None

        filepath = '/' + self.app.file.autoload_path()

        path = None
        for group in rules:
            if not filepath.startswith(group):
                continue
            for rule in rules.get(group):
                pattern = rule.get('pattern')
                if pattern is None:
                    continue
                r = re.compile(pattern)
                if r.search(filepath) is not None:
                    path = rule.get('path')
                    if not path.startswith('/'):
                        path = os.sep.join([project_type, 'files', path])
                    break
            if path is not None:
                break

        return path

    def suggest_snippets(self, user_input, locations):
        project_type = self.app.project.type()
        if project_type is None or self.app.composer.path() is None:
            return None

        rules = load_resource(os.sep.join([self.base_dir, project_type, 'snippets.json']), True)
        if rules is None:
            return None

        filepath = '/' + self.app.file.autoload_path()
        view = sublime.active_window().active_view()

        slashesInPlaceholders = re.compile(r'(?<!\\)\\(?![\\|\$])')
        snippets = []
        for group in rules:
            if not filepath.startswith(group):
                continue

            for snippet in rules.get(group):
                # @todo: move this prefix to config
                prefix = 'mt-'
                trigger = snippet.get('trigger')
                trigger = trigger[1:] if trigger.startswith('.') else prefix + trigger
                if not trigger.startswith(user_input):
                    continue

                pattern = snippet.get('pattern')
                if pattern is not None:
                    r = re.compile(pattern)
                    if r.search(filepath) is None:
                        continue

                for point in locations:
                    scope = snippet.get('scope')
                    if scope and not view.match_selector(point, scope):
                        continue

                    path = snippet.get('path')
                    if not path.startswith('/'):
                        path = os.sep.join([project_type, 'snippets', path])

                    contents = self.render(path)
                    contents = slashesInPlaceholders.sub(r'\\\\', contents);
                    snippets.append([trigger, contents])

        return snippets
