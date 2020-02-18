from django import forms


class ImagesGalleryForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': 'true'}))
