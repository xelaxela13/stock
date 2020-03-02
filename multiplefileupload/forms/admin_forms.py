from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from ..models import Image


class ImagesGalleryForm(forms.ModelForm):
    upload_images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': 'true'}))
    select_images = forms.ModelMultipleChoiceField(queryset=Image.objects.none(),
                                                   widget=FilteredSelectMultiple('Select images', True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select_images'].queryset = Image.objects.exclude(gallery=self.instance)

    def save(self, commit=True):
        queryset = self.cleaned_data.get('select_images')
        if queryset:
            queryset.all().update(gallery=self.instance)
        return super().save(commit)
