from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms.admin_forms import ImagesGalleryForm
from .models import Image, ImagesGallery
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail


@admin.register(Image)
class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    fields = ('file', 'slug', 'user', 'show', 'create_at')
    readonly_fields = ('user', 'create_at')
    list_display = ('snapshot', 'slug', 'create_at', 'show')

    def save_model(self, request, obj, form, change):
        if obj and not obj.user:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def snapshot(self, obj):
        return mark_safe(f'<div><img src="{get_thumbnail(obj.file, "80x80").url}"></div>')


@admin.register(ImagesGallery)
class ImagesGalleryAdmin(admin.ModelAdmin):
    fields = ('name', 'upload_images', 'images')
    form = ImagesGalleryForm
    list_display = ('name', 'images_count')
    filter_horizontal = ('images',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for image in request.FILES.getlist('upload_images'):
            Image.objects.create(file=image, user=request.user)
