from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from custom_auth.models import User


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This authentication backend allows the user to login with his email or username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        users = User.objects.filter(Q(username=username) | Q(email__iexact=username))

        for user in users:
            if user.check_password(password):
                return user
        if not users:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (see
            # https://code.djangoproject.com/ticket/20760)
            User().set_password(password)
