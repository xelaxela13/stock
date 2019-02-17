from django.apps import AppConfig


class StockConfig(AppConfig):
    name = 'stock'
    verbose_name = 'Склад'

    def ready(self):
        from stock import signals  # noqa