from os import path
from PIL import Image as PilImage
from io import BytesIO
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile


def file_name_extension(filename):
    name, extension = path.splitext(filename)
    return name.lower(), extension.lower()


def make_thumbnail(instance):
    image = PilImage.open(instance.file)
    thumb_size = instance.get_settings['THUMBNAIL_SIZE']
    image.thumbnail(thumb_size, PilImage.ANTIALIAS)
    thumb_name, thumb_extension = file_name_extension(instance.file.name)
    thumb_filename = thumb_name + '_thumb' + thumb_extension
    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False
    # Save thumbnail to in-memory file as BytesIO
    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)
    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()
    return True


def upload_file_to(instance, filename):
    name, extension = file_name_extension(filename)
    filename = '{}{}'.format(name[:20], extension)
    instance.file.name = filename
    if not make_thumbnail(instance):
        raise Exception('Could not create thumbnail - is the file type valid?')
    return instance.get_settings['IMAGE_PATH'] + filename


def upload_thumbnail_to(instance, filename):
    return instance.get_settings['THUMBNAIL_PATH'] + filename


class Image(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    file = models.ImageField(upload_to=upload_file_to)
    slug = models.SlugField(max_length=20, blank=True)
    thumbnail = models.ImageField(upload_to=upload_thumbnail_to, blank=True,
                                  help_text='Default thumbnail size 250x250 px, you can change it, '
                                            'rewrite THUMBNAIL_SIZE on settings, THUMBNAIL_SIZE should be a tuple.')
    deleted = models.BooleanField(default=False, help_text='Mark as deleted')
    show = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

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

    def clean(self):
        if not self.slug:
            self.slug = self.generate_slug()
        return super().clean()

    def generate_slug(self):
        return f'{self.pk}-{timezone.now().strftime("%Y-%m-%d")}'


class MultipleImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.SET_NULL)
