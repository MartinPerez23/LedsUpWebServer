from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class AllowInactiveAuthenticationBackend(ModelBackend):
    """
    Permite autenticar usuarios aunque estén inactivos (is_active=False).
    """
    def user_can_authenticate(self, user):
        return True