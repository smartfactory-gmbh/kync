from django.db import models

from project.mixins import TimestampableMixin

GROUP_TEMPLATE = """
########################################
# {}
########################################

{}
"""


class Group(TimestampableMixin, models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    persons = models.ManyToManyField("sync.Person", related_name="groups", blank=True)

    @property
    def output(self):
        keys = "\n".join([p.keys for p in self.persons.filter(active=True)])
        return GROUP_TEMPLATE.format(self.name.upper(), keys).strip()

    def sync_remote(self):
        for project in self.projects.all():
            project.sync_remote()

    def save(self, *args, **kwargs):
        super().save()
        self.sync_remote()

    def __str__(self):
        return str(self.name)
