from .file import File
from .project import Project
from .phpfile import Phpfile
from .composer import Composer
from .template import Template

class App:
    def __init__(self, filepath):
        self.filepath = filepath
        self.project = Project(self)
        self.composer = Composer(self)
        self.file = File(self)
        self.phpfile = Phpfile(self)
        self.template = Template(self)

    def render_template(self, template_path=None, base_dir=None):
        return self.template.render(template_path, base_dir)

    def render_snippet(self, snippet_path, base_dir=None):
        return self.template.render_snippet(snippet_path, base_dir)

    def suggest_snippets(self, prefix, locations):
        return self.template.suggest_snippets(prefix, locations)
