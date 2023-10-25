from django.contrib.auth.models import Group as BaseGroup


class Group(BaseGroup):
    class Meta:
        proxy = True
