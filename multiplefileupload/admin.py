from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms.admin_forms import ImagesGalleryForm
from .models import Image, ImagesGallery


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('file', 'slug', 'thumbnail', 'snapshot', 'user', 'deleted', 'show', 'create_at')
    readonly_fields = ('thumbnail', 'snapshot', 'user', 'create_at')
    list_display = ('snapshot', 'create_at')

    def save_model(self, request, obj, form, change):
        if obj and not obj.user:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def snapshot(self, obj):
        return mark_safe(f'<div><img src="{obj.thumbnail.url}" /></div>')


class ImagesGalleryInline(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(ImagesGallery)
class ImagesGalleryAdmin(admin.ModelAdmin):
    fields = ('gallery_name', 'images')
    form = ImagesGalleryForm
    inlines = (ImagesGalleryInline, )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        images = []
        for image in request.FILES.getlist('images'):
            images.append(Image(file=image, user=request.user, gallery=obj))

        if images:
            Image.objects.bulk_create(images)
