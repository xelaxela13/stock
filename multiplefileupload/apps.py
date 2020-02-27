from django.apps import AppConfig


class MultipleFileUploadConfig(AppConfig):
    name = 'multiplefileupload'

    def ready(self):
        from multiplefileupload import signals  # noqa
