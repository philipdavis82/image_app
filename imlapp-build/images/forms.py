from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = Inimg
        fields = ['name','main_input_img']