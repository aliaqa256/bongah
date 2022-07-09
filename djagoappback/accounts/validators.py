import re
from django.core import validators
from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r'^\+?1?\d{9,15}$'
    message = (
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


phone_validator = PhoneValidator()


