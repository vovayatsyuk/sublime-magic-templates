import sublime
import sublime_plugin

from .magento.env import Env
from .magento.phpfile import Phpfile
from .magento.template import Template

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = Env(self.view.file_name()).get_app()
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render(app + '/snippets/ifip')
        })

class GenerateContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render()
        })

class GenerateClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render('php/snippets/class')
        })

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render('php/snippets/classname')
        })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render('php/snippets/namespace')
        })

class GenerateContentOnFileCreation(sublime_plugin.EventListener):
    def on_load(self, view):
        # @todo: proper check for newly created file.
        # current logic returns true for opened empty file
        if view.file_name() is not None and view.size() == 0:
            view.run_command('insert_snippet', {
                'contents': Template(view.file_name()).render()
            })
