import sublime_plugin

from .mt.app import App

class GenerateContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contents = App(self.view.file_name()).render_template()
        if contents is not None:
            self.view.run_command('insert_snippet', {
                'contents': contents
            })

class GenerateContentOnFileCreation(sublime_plugin.EventListener):
    def on_load(self, view):
        # @todo: proper check for newly created file.
        # current logic returns true for opened empty file
        if view.file_name() is not None and view.size() == 0:
            contents = App(view.file_name()).render_template()
            if contents is not None:
                view.run_command('insert_snippet', {
                    'contents': contents
                })

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contents = App(self.view.file_name()).render_snippet('classname')
        if contents is not None:
            self.view.run_command('insert_snippet', {
                'contents': contents
            })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contents = App(self.view.file_name()).render_snippet('namespace')
        if contents is not None:
            self.view.run_command('insert_snippet', {
                'contents': contents
            })

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contents = App(self.view.file_name()).render_snippet('ifip')
        if contents is not None:
            self.view.run_command('insert_snippet', {
                'contents': contents
            })
