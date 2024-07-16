from django import forms
from .models import ImageInstance

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageInstance
        fields = ['imginst']

    def clean_imginst(self):
        imginst = self.cleaned_data.get('imginst')
        if imginst:
            valid_extensions = ['jpg', 'jpeg', 'png']
            extension = imginst.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('Unsupported file extension.')
        return imginst

ImageUploadFormSet = forms.modelformset_factory(ImageInstance, form=ImageUploadForm)
