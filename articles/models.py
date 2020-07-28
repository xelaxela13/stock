from django.db import models
from tinymce import models as tinymce_models


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField()
    view_count = models.PositiveSmallIntegerField(default=0)
    show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
