from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from .models import SystemInstance, Gig, Job


class JobInline(NestedTabularInline):
    model = Job
    extra = 0


# Register your models here.
class SystemInline(NestedStackedInline):
    model = SystemInstance
    inlines = (JobInline,)
    extra = 1


@admin.register(Gig)
class GigAdmin(NestedModelAdmin):
    inlines = (SystemInline,)