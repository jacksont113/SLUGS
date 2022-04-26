from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import Group
from gig.models import DEPARTMENTS
from tinymce.models import HTMLField
from django.utils import timezone


# Create your models here.
class Training(models.Model):
    """
    List of all trainings that have occurred/going to happen. Shows the department for training, date/time, trainer, system being trained, and the trainees. 
    """
    date = models.DateTimeField()
    dept = models.CharField(max_length=1, choices=DEPARTMENTS)
    location = models.ForeignKey(
        "location.Location", on_delete=models.SET_NULL, null=True, blank=True
    )
    capacity = models.IntegerField(null=True, blank=True)
    trainers = models.ManyToManyField("employee.Employee", related_name="trainers")
    attendees = models.ManyToManyField(
        "employee.Employee",
        through="training.Trainee",
        related_name="attendees",
        blank=True,
    )
    notes = HTMLField(null=True, blank=True)
    systems = models.ManyToManyField("equipment.System", blank=True)

    def __str__(self):
        return f"{self.get_dept_display()} Training - {timezone.localtime(self.date).strftime('%m/%d/%Y, %H:%M:%S')}"


class Trainee(models.Model):
    """
    List of available training spots with the trainee’s name, contact info, what training they are doing,
     and position at Binghamton Sound Stage and Lighting
    """
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    training = models.ForeignKey("training.Training", on_delete=models.CASCADE)
    position = models.ForeignKey(
        Group, default="New Hire", to_field="name", on_delete=models.PROTECT
    )
    shifts = GenericRelation("finance.Shift")

    def __str__(self):
        return f"{self.training}"


class TrainingRequest(models.Model):
    """
    List of all requests for training made by employees through the training tab in slugs. Shows if the training has been answered by a manager,
    the employee requesting the train with their email, and the date/time of the training. The page also allows you to make trainings and what systems the employee is training for.
    """
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    systems = models.ManyToManyField("equipment.System", blank=True)
    notes = models.TextField(null=True, blank=True, help_text="Be sure to include when you're free in the upcoming weeks to schedule the training")
    submitted = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f'{"[ANSWERED] " if self.answered else ""}{self.employee} - {timezone.localtime(self.submitted).strftime("%a, %d %b %Y %H:%M:%S %Z")}'
