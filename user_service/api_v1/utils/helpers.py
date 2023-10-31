import re
from django.core.exceptions import ValidationError


def validate_iso_code(value):
        regex = re.compile('^[A-Z]{3}$')
        if not regex.match(value):
            raise ValidationError('Invalid ISO country code')
