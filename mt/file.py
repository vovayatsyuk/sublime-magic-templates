import os


class File:
    def __init__(self, app):
        self.app = app
        self._psr4key = None
        self._psr4dir = None

    def path(self):
        return self.app.filepath

    def relative_path(self):
        return self.path().replace(self.app.project.root(), '').lstrip('/')

    def autoload_path(self):
        path = self.relative_path()
        subdir = self.psr4dir()
        if subdir:
            path = path.replace(subdir, '', 1)
        return path

    def filename(self):
        return os.path.basename(self.app.filepath)

    def basename(self):
        return os.path.splitext(os.path.basename(self.app.filepath))[0]

    def folder(self):
        return os.path.basename(os.path.dirname(self.app.filepath))

    def parent_folder(self):
        return os.path.basename(os.path.dirname(os.path.dirname(self.app.filepath)))

    def psr4key(self):
        if self._psr4key is not None:
            return self._psr4key

        psr4 = (self.app.composer.psr4(), [])[self.app.composer.psr4() is None]
        psr4dev = (self.app.composer.data('autoload-dev.psr-4'), [])[self.app.composer.data('autoload-dev.psr-4') is None]

        relative_path = self.relative_path()
        for psr4 in [psr4, psr4dev]:
            for key in psr4:
                if psr4[key]:
                    if relative_path.startswith(psr4[key]):
                        self._psr4key = key
                        self._psr4dir = psr4[key]
                        return key
                else:
                    self._psr4key = key
                    self._psr4dir = psr4[key]
                    return key

        return None

    def psr4dir(self):
        if self._psr4dir is not None:
            return self._psr4dir

        self.psr4key()

        return self._psr4dir
