from django.contrib import admin
from .forms.admin_forms import ImagesGalleryForm
from .models import Image, ImagesGallery
from sorl.thumbnail.admin import AdminImageMixin


@admin.register(Image)
class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    fields = ('file', 'slug', 'user', 'show', 'create_at', 'gallery')
    readonly_fields = ('user', 'create_at')
    list_display = ('file', 'slug', 'create_at', 'gallery', 'show')

    def save_model(self, request, obj, form, change):
        if obj and not obj.user:
            obj.user = request.user
        return super().save_model(request, obj, form, change)


class ImagesGalleryInline(AdminImageMixin, admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ('user',)


@admin.register(ImagesGallery)
class ImagesGalleryAdmin(admin.ModelAdmin):
    fields = ('name', 'upload_images', 'select_images')
    form = ImagesGalleryForm
    inlines = (ImagesGalleryInline, )
    list_display = ('name', 'images_count')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for image in request.FILES.getlist('upload_images'):
            Image.objects.create(file=image, user=request.user, gallery=obj)
