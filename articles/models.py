from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
