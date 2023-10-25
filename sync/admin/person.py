from django.contrib import admin

from ..models import Person
from .public_key import PublicKeyInline


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = ["name", "keys_count", "active"]

    list_filter = ["active"]

    inlines = [
        PublicKeyInline,
    ]
