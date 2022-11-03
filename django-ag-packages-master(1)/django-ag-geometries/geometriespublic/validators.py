
import bleach
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

def bleach_validator(text):
    cleaned_text = bleach.clean(text, strip=True, strip_comments=True, tags=[], attributes=[], styles=[])
    text = re.sub('[\r]','',text)
    cleaned_text = re.sub('&amp;','&',cleaned_text)
    if cleaned_text != text: #\r : \n , &amp : &
        raise ValidationError(
            gettext('Field cannot contain html tags.'),
            code='invalid'
        )
