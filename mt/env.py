import os

class Env:
    def __init__(self, app):
        self.app = app
        self._psr4key = None;

    def folder(self):
        return os.path.basename(os.path.dirname(self.app.filepath))

    def file(self):
        return os.path.splitext(os.path.basename(self.app.filepath))[0]

    def psr4key(self):
        if self._psr4key is not None:
            return self._psr4key

        module_path = self.app.composer.path().replace('composer.json', '')
        relative_path = self.app.filepath.replace(module_path, '')
        psr4 = self.app.composer.psr4()
        if psr4 is None:
            return None
        for key in psr4:
            subfolder = psr4[key].strip('/')
            if subfolder:
                if relative_path.startswith(subfolder):
                    self._psr4key = key
                    return key
            else:
                self._psr4key = key
                return key
        return None
