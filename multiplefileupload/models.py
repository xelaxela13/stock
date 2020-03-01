from os import path
from PIL import Image as PilImage
from io import BytesIO

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse


__ALL__ = ('Image', 'ImagesGallery')

AVAILABLE_EXTENSIONS = {
    '.jpg': 'JPEG',
    '.png': 'PNG',
    '.gif': 'GIF',
    '.jpeg': 'JPEG'
}


def extension_to_filetype(extension):
    return AVAILABLE_EXTENSIONS.get(extension, None)


def generate_filename(filename, is_thumb=False):
    name, extension = path.splitext(filename)
    return f'{name[:10]}_thumbnail{extension}' if is_thumb else f'{name[:10]}{extension}'


def upload_file_to(instance, filename):
    filename = generate_filename(filename)
    return f'{instance.get_settings["IMAGE_PATH"]}{filename}'


def upload_thumbnail_to(instance, filename):
    filename = generate_filename(filename, True)
    return f'{instance.get_settings["THUMBNAIL_PATH"]}{filename}'


class ImagesGallery(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return f'{self.pk} {self.name}'

    @property
    def images_count(self):
        return self.image_set.all().count()


class Image(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    gallery = models.ForeignKey(ImagesGallery, blank=True, null=True, on_delete=models.SET_NULL)
    file = models.ImageField(upload_to=upload_file_to)
    slug = models.SlugField(max_length=20, blank=True)
    thumbnail = models.ImageField(upload_to=upload_thumbnail_to, blank=True,
                                  help_text='Default thumbnail size 250x250 px, you can change it, '
                                            'rewrite THUMBNAIL_SIZE on settings, THUMBNAIL_SIZE should be a tuple.')
    show = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('image:image-slug', args=(self.slug, ))

    @property
    def get_settings(self):
        return {
            'THUMBNAIL_SIZE': getattr(settings, 'THUMBNAIL_SIZE', (250, 250)),
            'DELETE_MEDIA_FILES': getattr(settings, 'DELETE_MEDIA_FILES', True),
            'IMAGE_PATH': getattr(settings, 'IMAGE_PATH', f'images/{timezone.now().strftime("%Y/%m/%d")}/'),
            'THUMBNAIL_PATH': getattr(settings, 'THUMBNAIL_PATH', f'thumbnails/{timezone.now().strftime("%Y/%m/%d")}/')
        }

    def delete(self, *args, **kwargs):
        self.file.delete(self.get_settings['DELETE_MEDIA_FILES'])
        self.thumbnail.delete(self.get_settings['DELETE_MEDIA_FILES'])
        super().delete(*args, **kwargs)

    def generate_slug(self):
        return f'{self.pk}-{timezone.now().strftime("%Y-%m-%d")}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.slug:
            self.slug = self.generate_slug()
            self.save(update_fields=('slug',))

    def create_thumbnail(self):
        image = PilImage.open(self.file)
        thumb_size = self.get_settings['THUMBNAIL_SIZE']
        image.thumbnail(thumb_size, PilImage.ANTIALIAS)
        name, extension = path.splitext(self.file.name)
        thumb_filename = generate_filename(self.file.name)
        filetype = extension_to_filetype(extension)
        temp_thumb = BytesIO()
        try:
            image.save(temp_thumb, filetype)
            temp_thumb.seek(0)
            # set save=False, otherwise it will run in an infinite loop
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()))
        except (ValueError, IOError):
            pass
        temp_thumb.close()
