from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.forms.widgets import TextInput
from main.models import SiteDetails, SitePreferences, BGUser, UserPasswordRequests

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class SiteDetailsAdminForm(forms.ModelForm):
    class Meta:
        model = SitePreferences
        fields = '__all__'
        widgets = {
            'site_color': TextInput(attrs={'type': 'color'}),
        }


class SiteRedirectForm(forms.Form):
    site = forms.CharField(required=True)

class ResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)
    conflict = forms.BooleanField(required=False, initial=False)

    # "email" is valid from the technical point of view. We only want the form
    # to be valid if the email also corresponds to a registered user.
    def clean(self):
        cleaned_data = super().clean()
        user_email = cleaned_data.get('email')
        conflict = cleaned_data.get('conflict')

        if BGUser.objects.filter(email=user_email,is_active=True).exists():
            user = BGUser.objects.get(email=user_email)
            #if not user.site_groups.filter(burialgroundsite__schema_name__exact=connection.schema_name).exists():
                #self.add_error("email", "Your Email address doesn't correspond to a known, active, user on this site.")
        else:
            self.add_error("email", "Your Email address doesn't appear to correspond to a known, active, user. Please try again.")
            raise forms.ValidationError("User unknown.")


        if UserPasswordRequests.objects.filter(user=BGUser.objects.get(email=user_email)).exists():

            old_request = UserPasswordRequests.objects.get(user=BGUser.objects.get(email=user_email))

            if old_request.status == "Open":
                self.add_error("conflict", "You already have an open reset request.")
                raise forms.ValidationError("Request conflicts with existing.")

        return user_email