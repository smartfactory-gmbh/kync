from django.db import models

from project.mixins import TimestampableMixin


class Person(TimestampableMixin, models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    @property
    def keys(self):
        keys = list(self.public_keys.values_list("content", flat=True))
        return "\n".join([key.strip() for key in keys])

    @property
    def keys_count(self):
        return self.public_keys.count()

    def sync_remote(self):
        for project in self.projects.all():
            project.sync_remote()
        for group in self.groups.all():
            group.sync_remote()

    def save(self, *args, **kwargs):
        super().save()
        self.sync_remote()

    def __str__(self):
        return str(self.name)
