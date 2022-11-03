'''
Created on 28 Aug 2015

@author: achickermane
'''
from django import forms

class ShapeFileUpload(forms.Form):
    shp_file_zip = forms.FileField(
        label='Zip containing all shape files',
        required=False,
        # TODO: make this file upload thing better
        widget=forms.FileInput(attrs={'type':'file', 'class': 'file'})
    )