from django.contrib import admin
from .models import Notification, signupStatus
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    filter_horizontal = ("groups_to_send_to",)


@admin.register(signupStatus)
class signupStatus(admin.ModelAdmin):
    pass
