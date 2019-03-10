from import_export import resources, fields
from stock.models import Product
from django.core.exceptions import FieldDoesNotExist


class ProductResources(resources.ModelResource):
    total = fields.Field(column_name='total')
    price = fields.Field(column_name='price')
    unit = fields.Field(column_name='unit')

    class Meta:
        model = Product
        fields = ('sku', 'name', 'description', 'unit', 'total', 'price')
        export_order = ('sku', 'name', 'description')
        import_id_fields = ''

    def dehydrate_total(self, product):
        return Product.total_in_stock(product)

    def get_export_headers(self):
        headers = super().get_export_headers()
        verbose_headers = []
        for header in headers:
            try:
                if hasattr(self._meta.model._meta.get_field(header), 'verbose_name'):
                    verbose_headers.append(self._meta.model._meta.get_field(header).verbose_name)
                else:
                    verbose_headers.append(header)
            except FieldDoesNotExist:
                try:
                    verbose_headers.append(eval('self._meta.model.{}.short_description'.format(header)))
                except AttributeError:
                    verbose_headers.append(header)
        return verbose_headers
