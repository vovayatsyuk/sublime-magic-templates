from .composer import Composer

class Env:
    def __init__(self, file_path):
        self.file_path = file_path
        self.composer = Composer(file_path)

    def get_app(self):
        app = self.composer.get_type()
        stopwords = {
            'magento2-': 'magento2',
            'magento-': 'magento1'
        }
        for key in stopwords:
            if key in app:
                return stopwords[key]
        return None
