from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_percentage(level):
    if level < 0 or level > 100:   
        raise ValidationError(
            _('%(level)s is not a number between 0 and 100'),
            params={'level': level},
        )