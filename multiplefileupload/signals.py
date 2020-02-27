from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Image


@receiver(post_save, sender=Image, dispatch_uid='image_post_save')
def image_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    print(kwargs)
    st()
