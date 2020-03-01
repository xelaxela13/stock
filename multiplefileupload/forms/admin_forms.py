from django import forms


class ImagesGalleryForm(forms.ModelForm):
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': 'true'}))
