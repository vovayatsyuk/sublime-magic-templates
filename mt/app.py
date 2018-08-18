from .env import Env
from .phpfile import Phpfile
from .composer import Composer
from .template import Template

class App:
    def __init__(self, filepath):
        self.filepath = filepath
        self.composer = Composer(self)
        self.env = Env(self)
        self.phpfile = Phpfile(self)
        self.template = Template(self)

    def render_template(self, template_path=None, base_dir=None):
        return self.template.render(template_path, base_dir)

    def render_snippet(self, alias):
        return self.template.render_snippet(template_path, base_dir)
