from django.contrib.auth.forms import UserCreationForm

from custom_auth.fields import UsernameNullField


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        field_classes = {"username": UsernameNullField}
