from django import forms
from .models import *


class ImgForm(forms.ModelForm):
    class Meta:
        model   = Img
        fields  = ['name', 'kind', 'sort', 'file']