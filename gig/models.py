from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from tinymce.models import HTMLField
from django.contrib.auth.models import Group

import client.models as client
import location.models as location
import employee.models as employee

DEPARTMENTS = [
    ("L", "Lighting"),
    ("S", "Sound"),
    ("M", "Manager"),
    ("O", "Other"),
    ("T", "Staging"),
]


class Gig(models.Model):
    """
    List of all Binghamton Sound Stage and Lighting Gigs. This page allows you to create gigs and look at previously created gigs.
    Shows the name of the show, organization, date, and status (i.e. Archived, Cancelled). This page also has the ability to allow managers to staff the show, send staffing emails, 
    choose the set-up time, start time, end time, organization, lead contact, the location of the show, and the packages with number of employees needed for the show. The gig page also has manager notes and employee notes to show when staffing. 
    """
    name = models.CharField(max_length=200)
    notes = HTMLField(
        blank=True,
        null=True,
        help_text="This will show up on the showview page and the estimate as 'ATTN ENG'",
    )
    manager_only_notes = HTMLField(blank=True, null=True)
    setup_by = models.DateTimeField(verbose_name="Setup By")
    start = models.DateTimeField(verbose_name="Gig start time")
    end = models.DateTimeField(verbose_name="Gig end time")
    org = models.ForeignKey(client.Organization, models.PROTECT)
    contact = models.ForeignKey(client.OrgContact, models.PROTECT, null=True)
    location = models.ForeignKey(location.Location, models.PROTECT)
    day_of_show_notes = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    available_for_signup = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date Available for Signup",
        help_text="If left blank, this value will be set to 7 days prior to the start date.",
    )
    systems = models.ManyToManyField("equipment.System", through="SystemInstance")

    def get_staff_link(self):
        return format_html(
            "<a href='%s'>%s</a>"
            % (reverse("admin:gig_gig_staff", args=(self.id,)), "Staff Show")
        )

    def send_staffing_email(self):
        return format_html(
            "<a href='%s'>%s</a>"
            % (reverse("admin:gig_gig_email", args=(self.id,)), "Send staffing email")
        )

    def __str__(self):
        return (
            self.name
            + " - "
            + str(self.org)
            + " - "
            + str(timezone.localtime(self.start).strftime("%m/%d/%Y"))
            + (" [UNPUBLISHED]" if not self.published else "")
            + (" [ARCHIVED]" if self.archived else "")
        )  # noop

    def save(self, *args, **kwargs):
        if self.available_for_signup is None:
            self.available_for_signup = self.start - timezone.timedelta(days=7)
        super().save(*args, **kwargs)


class LoadIn(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    department = models.CharField(choices=DEPARTMENTS, max_length=1)
    shop_time = models.DateTimeField()
    load_in = models.DateTimeField()
    load_out = models.DateTimeField()

    def __str__(self):
        return f"{self.department} - {self.gig}"


class SystemInstance(models.Model):
    system = models.ForeignKey("equipment.System", on_delete=models.PROTECT)
    addons = models.ManyToManyField(
        "equipment.SystemAddon", through="gig.AddonInstance", blank=True
    )
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    employees = models.ManyToManyField(employee.Employee, through="Job")

    class Meta:
        verbose_name = "Rented System"
        verbose_name_plural = "Rented Systems"

    def __str__(self):
        return f"{self.system}"


class AddonInstance(models.Model):
    addon = models.ForeignKey("equipment.SystemAddon", on_delete=models.CASCADE)
    systemInstance = models.ForeignKey("gig.SystemInstance", on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)
    qty = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Addon"
        verbose_name_plural = "Addons"


class Job(models.Model):
    """
    List of all Binghamton Sound Stage and Lighting positions for shows. 
    This page shows the name of the event and the employee who was staffed with their email. 
    This page shows each job individually showing multiple jobs for each show. 
    """
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        employee.Employee, on_delete=models.SET_NULL, null=True, blank=True
    )
    position = models.ForeignKey(Group, on_delete=models.PROTECT)
    linked_system = models.ForeignKey(
        SystemInstance, on_delete=models.PROTECT, null=True, blank=True
    )
    department = models.CharField(choices=DEPARTMENTS, max_length=1)
    is_test = models.BooleanField(default=False)
    shifts = GenericRelation("finance.Shift")

    def __str__(self):
        return f"{self.gig.name} - {self.gig.org}"


class JobInterest(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    employee = models.ForeignKey(employee.Employee, on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.job.gig}"
