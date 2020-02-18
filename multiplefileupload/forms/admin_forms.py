from django import forms


class ImagesGalleryInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs = {'multiple': 'true'}
