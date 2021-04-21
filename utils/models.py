from django.db import models
from tinymce.models import HTMLField

from django.contrib.auth.models import Group


# Create your models here.
class Notification(models.Model):
    MESSAGE_TYPES = [
        ("normal bg-white text-black", "Normal"),
        ("bg-green-500", "Success"),
        ("bg-yellow-500", "Warning"),
        ("bg-red-500", "Danger/Error"),
    ]
    name = models.CharField(max_length=150)
    groups_to_send_to = models.ManyToManyField(
        Group,
        blank=True,
        help_text="Send the notification to the following groups.",
    )
    message = HTMLField()
    message_type = models.CharField(
        choices=MESSAGE_TYPES, max_length=64, default="normal"
    )
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_published) + " - " + self.name


class signupStatus(models.Model):
    is_open = models.BooleanField()

    def __str__(self):
        return f'Signup is currently {"Open" if self.is_open else "Closed"}'


class onboardingStatus(models.Model):
    is_open = models.BooleanField()

    def __str__(self):
        return f'User onboarding is currently {"Open" if self.is_open else "Closed"}'