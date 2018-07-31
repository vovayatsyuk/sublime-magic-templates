import sublime
import sublime_plugin

from .magento.phpfile import Phpfile
from .magento.template import Template

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            from IpAddress.ipaddress.IpAddress import IpAddress as IpAddress
        except ImportError:
            return sublime.error_message("Please install IpAddress plugin.")

        ip = IpAddress.instance().get()

        # assume it's a Magento 2 if namespace is found
        namespace = self.view.find_by_selector('meta.namespace.php')
        if namespace:
            command = "\\Magento\\Framework\\App\\ObjectManager::getInstance()->get('\\Magento\\Framework\\HTTP\\PhpEnvironment\\RemoteAddress')->getRemoteAddress()"
        else:
            command = "Mage::helper('core/http')->getRemoteAddr()"

        template = "if ('%s' === " + command + ") {\n    $0\n}"

        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region).replace('$', '\\$')
                self.view.run_command('insert_snippet', {'contents': template % (ip)})
                self.view.run_command('insert_snippet', {'contents': text})
            else:
                self.view.run_command('insert_snippet', {'contents': template % (ip)})

class GenerateContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render()
        })

class GenerateClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render('php/class')
        })

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render('php/classname')
        })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render('php/namespace')
        })

class GenerateContentOnFileCreation(sublime_plugin.EventListener):
    def on_load(self, view):
        # @todo: proper check for newly created file.
        # current logic returns true for opened empty file
        if view.file_name() is not None and view.size() == 0:
            view.run_command('insert_snippet', {
                'contents': Template(view.file_name()).render()
            })
