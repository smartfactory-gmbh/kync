from django.core.management.base import BaseCommand
from sentry_sdk import capture_message


class Command(BaseCommand):
    help = "Triggers a Sentry message arbitrarily"

    def handle(self, *args, **options):
        capture_message("This is a message triggered from backend for testing purpose")
