from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image, MultipleImage


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('file', 'slug', 'thumbnail', 'snapshot', 'user', 'deleted', 'show', 'create_at')
    readonly_fields = ('thumbnail', 'snapshot', 'user', 'create_at')

    def save_model(self, request, obj, form, change):
        if obj and not obj.user:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def snapshot(self, obj):
        return mark_safe(f'<div><img src="{obj.thumbnail.url}" /></div>')


class ImageInlines(admin.TabularInline):
    model = Image


@admin.register(MultipleImage)
class MultipleImageAdmin(admin.ModelAdmin):
    pass
