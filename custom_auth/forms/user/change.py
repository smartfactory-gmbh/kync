from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from custom_auth.fields import UsernameNullField


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        field_classes = {"username": UsernameNullField}
