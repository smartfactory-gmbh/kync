import logging
from collections.abc import Iterator
from contextlib import contextmanager

from django.db import models
from paramiko.client import AutoAddPolicy, SSHClient

from project.mixins import TimestampableMixin
from sync.utils import get_kync_private_key_location, get_kync_public_key

logger = logging.getLogger(__name__)

# Banner generated with https://manytools.org/hacker-tools/ascii-banner/
FILE_HEADER = """
#  888    d8P
#  888   d8P
#  888  d8P
#  888d88K     888  888 88888b.   .d8888b
#  8888888b    888  888 888 "88b d88P"
#  888  Y88b   888  888 888  888 888
#  888   Y88b  Y88b 888 888  888 Y88b.
#  888    Y88b  "Y88888 888  888  "Y8888P
#                   888
#              Y8b d88P
#               "Y88P"

# Project name: {}
# Host: {}
# Environment: {}
"""

OUTPUT = """
{}

{}

# Kync key (always included)
############################

{}
"""


class Environment(TimestampableMixin, models.Model):

    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    ssh_user = models.CharField(max_length=50, default="ubuntu")

    project = models.ForeignKey("sync.Project", related_name="environments", on_delete=models.CASCADE)

    comment = models.TextField(help_text="This will be added in the key files on server", blank=True)
    internal_comment = models.TextField(help_text="Only for administration", blank=True)

    @property
    def _header(self):
        header = FILE_HEADER.format(self.project.name, self.host, self.name)

        if self.comment:
            header += f"# Comment: {self.comment}"

        return header.strip()

    @property
    def _keys(self):
        group_keys = "\n".join([group.output for group in self.project.groups.filter(active=True)])
        person_keys = "\n".join([person.keys for person in self.project.persons.filter(active=True)])

        results = []

        if person_keys:
            results.append(person_keys)
        if group_keys:
            results.append(group_keys)

        return "\n\n".join(results).strip()

    @property
    def output(self):
        return OUTPUT.format(self._header, self._keys, get_kync_public_key()).strip() + "\n"

    @contextmanager
    def _connect(self) -> Iterator[SSHClient]:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.host, username=self.ssh_user, key_filename=get_kync_private_key_location())
        try:
            yield client
        finally:
            client.close()

    def sync_remote(self):
        from ..tasks import update_remote_env_keys

        update_remote_env_keys.apply_async(args=[self.pk])

    def write_authorized_keys(self):
        with self._connect() as client:
            sftp = client.open_sftp()
            file = sftp.file(f"/home/{self.ssh_user}/.ssh/authorized_keys", "w", -1)
            file.write(self.output)
            sftp.close()
            logger.info(f"authorized_keys file was written at {self.host}")
            logger.debug(self.output)

    def save(self, *args, skip_remote_sync=False, **kwargs):
        super().save(*args, **kwargs)
        if not skip_remote_sync:
            self.sync_remote()

    def __str__(self):
        return str(self.name)
