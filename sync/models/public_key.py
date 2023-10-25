from django.db import models

from project.mixins import TimestampableMixin


class PublicKey(TimestampableMixin, models.Model):
    person = models.ForeignKey("sync.Person", related_name="public_keys", on_delete=models.PROTECT)
    content = models.TextField()

    def sync_remote(self):
        self.person.sync_remote()

    def save(self, *args, **kwargs):
        super().save()
        self.sync_remote()

    def __str__(self):
        return f"{str(self.person)}: {self.content[:8]}...{self.content[-8:]}"
