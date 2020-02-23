import pytest
from io import StringIO
from PIL import Image as PilImage

from django.urls import reverse
from django.core.files.base import File
from django.contrib.auth import get_user_model
from .models import Image


class TestImageAdmin:
    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = PilImage.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_add_image(self, admin_client):
        response = admin_client.get(reverse('admin:multiplefileupload_image_'))
        st()
        # self.assertEqual(lion.speak(), 'The lion says "roar"')

