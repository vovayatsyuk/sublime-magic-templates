from .composer import Composer

class Env:
    def __init__(self, file_path):
        self.file_path = file_path
        self.composer = Composer(file_path)

    def get_app(self):
        app = self.composer.get_type()
        if app is not None:
            knowntypes = {
                'magento2-': 'magento2',
                'magento-': 'magento1'
            }
            for key in knowntypes:
                if key in app:
                    return knowntypes[key]

        # @todo: try to detect by `require` section

        # @todo: fallback to default value from config

        return None
