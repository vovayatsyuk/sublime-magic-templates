import sublime_plugin

from .mt.app import App

def insert_snippet(view, contents):
    if contents is None:
        return;
    view.run_command('insert_snippet', {
        'contents': contents
    })

class GenerateContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert_snippet(self.view, App(self.view.file_name()).render_template())

class GenerateContentOnFileCreation(sublime_plugin.EventListener):
    def on_load(self, view):
        # @todo: proper check for newly created file.
        # current logic returns true for opened empty file
        if view.file_name() is not None and view.size() == 0:
            insert_snippet(view, App(view.file_name()).render_template())

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert_snippet(self.view, App(self.view.file_name()).render_snippet('classname'))

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert_snippet(self.view, App(self.view.file_name()).render_snippet('namespace'))

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert_snippet(self.view, App(self.view.file_name()).render_snippet('ifip'))

class MagicSnippets(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.file_name() is not None:
            return App(view.file_name()).suggest_snippets(prefix, locations)
