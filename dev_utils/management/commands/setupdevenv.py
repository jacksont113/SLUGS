from SLUGS.settings import env
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from utils.models import signupStatus, onboardingStatus

from finance.models import Wage


class Command(BaseCommand):
    help = "Sets up environment for development (create Manager group, ...)"

    def handle(self, *args, **options):
        # Create signup status
        try:
            signupStatus.objects.get_or_create(is_open=False)
        except Exception:
            print("Could not generate signup status")
        # Create onboarding status
        try:
            onboardingStatus.objects.get_or_create(is_open=False)
        except Exception:
            print("Could not generate onboarding status")
        # Create deafult wages and groups
        try:
            try:
                WAGES = [
                    ("Tech", 11.80),
                    ("Engineer", 11.90),
                    ("Senior Engineer", 12.00),
                    ("Manager", 12.20),
                    ("GM & FD", 13.00),
                    ("Stage", 15.00)
                ]
                for wage_name, rate in WAGES:
                    Wage.objects.get_or_create(name=wage_name, hourly_rate=rate)
            except Exception:
                print("Could not create wages")
            try:
                GROUPS = [
                    ("Bi-Amping Engineer", "Engineer"),
                    ("Conditional Hire", "Tech"),
                    ("Junior Engineer", "Engineer"),
                    ("Large Engineer", "Engineer"),
                    ("Lighting", "Tech"),
                    ("Lighting Load in / out", "Tech"),
                    ("Lighting Tech", "Tech"),
                    ("Manager", "Manager"),
                    ("Medium Engineer", "Engineer"),
                    ("New Hire", "Tech"),
                    ("Probie - Lighting", "Tech"),
                    ("Probie - Sound", "Tech"),
                    ("Senior Engineer", "Senior Engineer"),
                    ("Small Engineer", "Engineer"),
                    ("Sound", "Tech"),
                    ("Sound Load in / out", "Tech"),
                    ("Sound Tech", "Tech"),
                ]
                for group_name, rate in GROUPS:
                    print(group_name, rate)
                    wage = Wage.objects.get(name=rate)
                    Group.objects.get_or_create(name=group_name, hourly_rate=wage)
            except Exception:
                print("Could not create all groups required")
        except Exception:
            print("Was not able to create wages and groups")
