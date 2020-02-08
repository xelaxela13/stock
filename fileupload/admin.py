from fileupload.models import Picture
from django.contrib import admin


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    fields = ('file', 'slug', 'thumbnail', 'user', 'deleted', 'show', 'create_at')
    readonly_fields = ('thumbnail', 'user', 'create_at')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
