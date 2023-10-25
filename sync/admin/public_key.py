from django.contrib import admin

from ..models import PublicKey


class PublicKeyInline(admin.TabularInline):
    extra = 1
    model = PublicKey
