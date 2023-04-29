import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UppercaseLowercaseNumbersSymbolsValidator:
    def __init__(self):
        self.uppercase_regex = re.compile(r'[A-Z]')
        self.lowercase_regex = re.compile(r'[a-z]')
        self.number_regex = re.compile(r'\d')
        self.symbol_regex = re.compile(r'[!@#$%^&*(),.?":{}|<>]')

    def validate(self, password, user=None) -> None:
        if not self.uppercase_regex.search(password):
            raise ValidationError(_("La contraseña debe contener al menos una letra mayúscula."))
        if not self.lowercase_regex.search(password):
            raise ValidationError(_("La contraseña debe contener al menos una letra minúscula."))
        if not self.number_regex.search(password):
            raise ValidationError(_("La contraseña debe contener al menos un número."))
        if not self.symbol_regex.search(password):
            raise ValidationError(_("La contraseña debe contener al menos un símbolo."))

    def get_help_text(self) -> str:
        return _("La contraseña debe tener al menos una letra mayúscula, una letra minúscula, un número y un símbolo.")
