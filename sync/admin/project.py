from django.contrib import admin

from ..models import Project
from .environment import EnvironmentInline


@admin.action(description="Sync remote environments")
def sync_remote(modeladmin, request, queryset):
    for project in queryset.all():
        project.sync_remote()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ["groups", "persons"]

    inlines = [
        EnvironmentInline,
    ]

    actions = [sync_remote]

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions
