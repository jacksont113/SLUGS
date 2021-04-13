from SLUGS.settings import env
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from utils.models import signupStatus


class Command(BaseCommand):
    help = "Sets up environment for development (create Manager group, ...)"

    def handle(self, *args, **options):
        # Create manager group
        try:
            Group.objects.get_or_create(name="Manager")
        except (Exception):
            print("Could not create group: `Manager`")
        # Create signup status
        try:
            signupStatus.objects.get_or_create(is_open=False)
        except (Exception):
            print("Could not generate signup status")
