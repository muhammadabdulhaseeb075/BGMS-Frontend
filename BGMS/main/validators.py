
import bleach
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext
import os
from django.core.exceptions import ValidationError


def bleach_validator(text):
    cleaned_text = bleach.clean(text, strip=True, strip_comments=True, tags=[], attributes=[], styles=[])
    text = re.sub('[\r]','',text)
    cleaned_text = re.sub('&amp;','&',cleaned_text)
    if cleaned_text != text: #\r : \n , &amp : &
        raise ValidationError(
            gettext('Field cannot contain html tags.'),
            code='invalid'
        )

def email_validator(text):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, text):
        raise ValidationError(
            gettext('Invalid email structure.'),
            code='invalid'
        )

# Enables checking for inclusion of a symbol in user passwords
# (called in settings).
class SymbolValidator(object):

    def validate(self, password, user=None):

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                gettext("The password must contain at least 1 symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?."),
                code='password_no_symbol',)

    def get_help_text(self):

        return gettext(
            "Your password must contain at least 1 symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?.")

def validate_file_extension(value):
    """
    Only Accepts .pdf files
    """
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')