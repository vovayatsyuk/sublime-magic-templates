import os

class File:
    def __init__(self, app):
        self.app = app
        self._psr4key = None

    def path(self):
        return self.app.filepath

    def relative_path(self):
        return self.path().replace(self.app.project.root(), '').lstrip('/')

    def autoload_path(self):
        path = self.relative_path()
        subdir = self.app.composer.psr4().get(self.psr4key())
        if subdir:
            path = path.replace(subdir, '', 1)
        return path

    def basename(self):
        return os.path.splitext(os.path.basename(self.app.filepath))[0]

    def folder(self):
        return os.path.basename(os.path.dirname(self.app.filepath))

    def psr4key(self):
        if self._psr4key is not None:
            return self._psr4key

        psr4 = self.app.composer.psr4()
        if psr4 is None:
            return None

        relative_path = self.relative_path()

        for key in psr4:
            if psr4[key]:
                if relative_path.startswith(psr4[key]):
                    self._psr4key = key
                    return key
            else:
                self._psr4key = key
                return key

        return None
