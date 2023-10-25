import logging

from django.db import models

from project.mixins import TimestampableMixin

logger = logging.getLogger(__name__)


class Project(TimestampableMixin, models.Model):
    name = models.CharField(max_length=255)

    groups = models.ManyToManyField("sync.Group", related_name="projects", blank=True, default="")
    persons = models.ManyToManyField("sync.Person", related_name="projects", blank=True, default="")

    def sync_remote(self):
        for env in self.environments.all():
            env.sync_remote()

    def __str__(self):
        return str(self.name)
