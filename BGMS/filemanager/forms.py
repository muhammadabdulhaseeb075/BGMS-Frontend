from django.forms import ModelForm
from filemanager.models import File

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'url']