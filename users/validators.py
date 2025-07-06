import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&.#_-]).{8,}$"
        if not re.match(pattern, password):
            raise ValidationError(
                _("La contraseña debe tener mínimo 8 caracteres, incluyendo mayúsculas, minúsculas, números y al menos un caracter especial (@$!%*?&.#_-)."),
                code="invalid_password",
            )

    def get_help_text(self):
        return _(
            "La contraseña debe tener mínimo 8 caracteres, incluyendo mayúsculas, minúsculas, números y al menos un caracter especial (@$!%*?&.#_-).")
