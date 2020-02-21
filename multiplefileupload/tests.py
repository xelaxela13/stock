from io import StringIO
from PIL import Image

from django.core.files.base import File
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Image


class ImageModelTest(TestCase):
    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        User = get_user_model()
        user = User.objects.get_or_create(email='test@mail.com')[0]
        Image.objects.get_or_create(file=self.get_image_file(), user=user)


    def test_clean(self):
        image = Image.objects.last()
        st()
        # self.assertEqual(lion.speak(), 'The lion says "roar"')

