class Env:
    def __init__(self, app):
        self.file_path = app.filepath
        self.composer = app.composer

    def get_app(self):
        app_type = self.composer.get_type()
        if app_type is not None:
            knowntypes = {
                'magento2-': 'magento2',
                'magento-': 'magento1'
            }
            for key in knowntypes:
                if key in app_type:
                    return knowntypes[key]

        # @todo: try to detect by `require` section

        # @todo: detect by `current_syntax` (php, etc)

        # @todo: fallback to default value from config
        return 'magento2'
