from django import forms

from .models import UploadModel


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ('file',)