from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from tinymce.models import HTMLField


import client.models as client
import location.models as location
import employee.models as employee

DEPARTMENTS = [
    ("L", "Lighting"),
    ("S", "Sound"),
    ("M", "Manager"),
    ("O", "Other"),
]


class Gig(models.Model):
    name = models.CharField(max_length=200)
    notes = HTMLField()
    load_in_lighting = models.DateTimeField(blank=True, null=True)
    load_in_sound = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(verbose_name="Gig start time")
    end = models.DateTimeField(verbose_name="Gig end time")
    load_out_lighting = models.DateTimeField(blank=True, null=True)
    load_out_sound = models.DateTimeField(blank=True, null=True)
    org = models.ForeignKey(client.Organization, models.PROTECT)
    contact = models.ForeignKey(client.OrgContact, models.PROTECT, null=True)
    location = models.ForeignKey(location.Location, models.PROTECT)
    day_of_show_notes = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    systems = models.ManyToManyField('equipment.System', through="SystemInstance")

    def get_assign_link(self):
        return format_html(
            "<a href='%s'>%s</a>"
            % (reverse("admin:gig_gig_assign", args=(self.id,)), "Assign Staffing")
        )

    def __str__(self):
        return self.name + " - " + str(self.org) + " - " + str(self.start.date())

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)


class SystemInstance(models.Model):
    rented_for = models.DurationField(verbose_name="# Hours rented")
    system = models.ForeignKey('equipment.System', on_delete=models.PROTECT)
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    employees = models.ManyToManyField(employee.Employee, through="Job")


class Job(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(employee.Employee, on_delete=models.SET_NULL, null=True)
    linked_system = models.ForeignKey(SystemInstance, on_delete=models.PROTECT)
    department = models.CharField(choices=DEPARTMENTS, max_length=1)


class JobInterest(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    employee = models.ForeignKey(employee.Employee, on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now=True)


class Shift(models.Model):
    job = models.ForeignKey(Job, on_delete=models.PROTECT)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    processed = models.BooleanField(default=False)
    contested = models.BooleanField(default=False)
