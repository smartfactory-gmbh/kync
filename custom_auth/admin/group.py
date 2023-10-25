from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group as BaseGroup

from custom_auth.models import Group

from .user import UserInlineAdmin

admin.site.unregister(BaseGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    inlines = [
        UserInlineAdmin,
    ]
