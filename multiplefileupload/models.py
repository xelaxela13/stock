from os import path

from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from sorl.thumbnail import ImageField

__ALL__ = ('Image', 'ImagesGallery')


def upload_file(instance, filename):
    name, extension = path.splitext(filename)
    return f'{instance.get_settings["IMAGE_PATH"]}{name[:10]}{extension}'


class ImagesGallery(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return f'{self.pk} {self.name}'

    @property
    def images_count(self):
        return self.image_set.all().count()

    @classmethod
    def cache_key(cls, name):
        return f'images_from_{name}'

    @classmethod
    def get_images_from_gallery(cls, name):
        images = cache.get(cls.cache_key(name))
        if not images:
            try:
                images = cls.objects.get(name=name).image_set.filter(show=True)
            except cls.DoesNotExist:
                return cls.objects.none()
            except cls.MultipleObjectsReturned:
                images = cls.objects.filter(name=name).last().image_set.filter(show=True)
            finally:
                cache.set(cls.cache_key(name), images)
        return images

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        cache.delete(self.cache_key(self.name))


class Image(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    gallery = models.ForeignKey(ImagesGallery, blank=True, null=True, on_delete=models.SET_NULL)
    file = ImageField(upload_to=upload_file)
    slug = models.SlugField(max_length=20, blank=True)
    show = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('image:image-slug', args=(self.slug, ))

    @property
    def get_settings(self):
        return {
            'DELETE_MEDIA_FILES': getattr(settings, 'DELETE_MEDIA_FILES', True),
            'IMAGE_PATH': getattr(settings, 'IMAGE_PATH', f'images/{timezone.now().strftime("%Y/%m/%d")}/'),
        }

    def delete(self, *args, **kwargs):
        self.file.delete(self.get_settings['DELETE_MEDIA_FILES'])
        super().delete(*args, **kwargs)

    def generate_slug(self):
        return f'{self.pk}-{timezone.now().strftime("%Y-%m-%d")}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.slug:
            self.slug = self.generate_slug()
            self.save(update_fields=('slug',))
