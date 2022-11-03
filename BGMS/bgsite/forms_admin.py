
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm

class TenantUserForm(ModelForm):

    class Meta:
        model = User
        exclude = ('password',)
        
class UploadPhotosForm(forms.Form):
    csv_file = forms.FileField(help_text='Please add the following titles for column 1: "memorial_number" and for column 2: "filename"', required=False, widget=forms.FileInput(attrs={'type':'file', 'class': '', 'accept': '.csv'}))

class UploadBurialRecordPhotosForm(forms.Form):
    photosFiles = forms.FileField(required=False)

class UploadOwnershipRegisterPhotosForm(forms.Form):
    photosFiles = forms.FileField(required=False)

class addPermissionsForm(forms.Form):
    username = forms.CharField(required=True)

class sendEmailInvitationForm(forms.Form):
    email_invitation = forms.EmailField(required=True)
