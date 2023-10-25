from django.contrib.auth.forms import UsernameField as BaseUsernameField


class UsernameNullField(BaseUsernameField):
    def to_python(self, value):
        if value:
            return super().to_python(value)

        return super(BaseUsernameField, self).to_python(value)
