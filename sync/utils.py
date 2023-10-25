import os

from django.conf import settings


def get_kync_private_key_location():
    return os.path.join(settings.SSH_KEYPAIR_LOCATION, settings.SSH_KEYPAIR_NAME)


def get_kync_public_key():
    with open(f"{get_kync_private_key_location()}.pub", "r") as f:
        return f.read().strip()
