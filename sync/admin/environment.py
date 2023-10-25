from django.contrib import admin

from ..models import Environment


class EnvironmentInline(admin.TabularInline):
    model = Environment
