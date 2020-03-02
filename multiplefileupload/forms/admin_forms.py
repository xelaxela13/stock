from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from ..models import Image


class ImagesGalleryForm(forms.ModelForm):
    upload_images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': 'true'}))
    select_images = forms.ModelMultipleChoiceField(queryset=Image.objects.none(),
                                                   widget=FilteredSelectMultiple('Select images', True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select_images'].queryset = Image.objects.exclude(gallery__in=(self.instance,))
