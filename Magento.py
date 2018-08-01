import sublime
import sublime_plugin

from .magento.template import Template

class GenerateContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render()
        })

class GenerateContentOnFileCreation(sublime_plugin.EventListener):
    def on_load(self, view):
        # @todo: proper check for newly created file.
        # current logic returns true for opened empty file
        if view.file_name() is not None and view.size() == 0:
            view.run_command('insert_snippet', {
                'contents': Template(view.file_name()).render()
            })

class GenerateClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render_snippet('class')
        })

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render_snippet('classname')
        })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render_snippet('namespace')
        })

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render_snippet('ifip')
        })
