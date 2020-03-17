from django import forms


class ImagesGalleryForm(forms.ModelForm):
    upload_images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': 'true'}))
