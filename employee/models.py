import os
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField


class EmployeeManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Employee(AbstractUser):
    """
    List of every employee that works or have worked for Binghamton Sound Stage and Lighting. 
    This list shows their name, preferred name, b-number, contacts via email and phone number, date hired, if they are a current employee, manager, or system admin. 
    This also shows if the employees outstanding :model:`employee.paperwork` .
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bnum = models.CharField(null=True, max_length=12, verbose_name="B Number")
    phone_number = PhoneNumberField(null=True)
    is_grad_student = models.BooleanField(default=False)
    graduation_year = models.IntegerField(blank=True, null=True)
    employee_notes = HTMLField(
        blank=True,
        null=True,
        help_text='Think of this as a "permanent record". Note anything important about this employee that should stick around. DO NOT delete anything from this unless you know what you\'re doing.',
    )
    paperwork = models.ManyToManyField(
        to="employee.Paperwork", through="employee.PaperworkForm"
    )
    is_active = models.BooleanField(default=False, verbose_name="Current Employee")
    is_staff = models.BooleanField(default=False, verbose_name="Manager")
    is_superuser = models.BooleanField(default=False, verbose_name="System Admin")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    objects = EmployeeManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def paperwork_outstanding(self):
        papers = []
        for form in PaperworkForm.objects.filter(
            employee=self.pk, processed=False
        ).all():
            papers.append(form.form.form_name)
        return ", ".join(papers)


class OfficeHours(models.Model):
    position = models.ForeignKey(
        Group, default="Manager", to_field="name", on_delete=models.PROTECT
    )
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    shifts = GenericRelation("finance.Shift")

    class Meta:
        verbose_name_plural = "Office Hours"

    def __str__(self):
        return "Office Hours"


class PaperworkForm(models.Model):
    """
    Gives a list of all :model:`employee.paperwork` documents from every employee in order of upload date *(not including timesheets)*. 
    This includes the :model:`employee.employee` name, email, document updated, and last edit date. 
    You also have the ability to add paperwork forms to individuals in this model. 
    """
    def user_dir_path(instance, filename):
        fileName, fileExtension = os.path.splitext(filename)
        return f"uploads/{instance.employee.bnum}/{instance.employee.bnum}_{instance.employee.first_name[0].upper()}{instance.employee.last_name}_{str(instance.form)}{fileExtension}"  # noqa

    form = models.ForeignKey("employee.Paperwork", on_delete=models.PROTECT)
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    pdf = models.FileField(upload_to=user_dir_path, blank=True, null=True)
    uploaded = models.DateTimeField(blank=True, null=True)
    requested = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.form}"


class Paperwork(models.Model):
    """
    List of all :model:`employee.paperwork` paperwork *(not including timesheets)*. 
    Gives the list of people who were sent the paperwork and if it has been digitally signed or uploaded. 
    This also gives access to the uploaded paperwork from every employee. 
    You also have the ability to add paperwork from this model. 
    """
    form_name = models.CharField(max_length=256)
    form_pdf = models.FileField(upload_to="forms/")
    uploaded = models.DateTimeField(auto_now_add=True)
    handed_in = models.CharField(max_length=512, null=True, blank=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form_name} {self.edited.year}"

    def associated_forms(self):
        ret = ""
        for form in (
            PaperworkForm.objects.filter(form=self.pk, employee__is_active=True)
            .order_by("processed")
            .all()
        ):
            line = "<div style='margin: .25rem 0 .25rem 0'>"
            line += (
                f"<a href='/media/{form.pdf}'>{form}</a>"
                if form.pdf
                else f"<span>{form}</span>"
            )
            line += "<b> - NOT PROCESSED</b>" if not form.processed else ""
            line += "</div><br>"
            ret += line
        return format_html(ret)

    class Meta:
        verbose_name = "Paperwork"
        verbose_name_plural = "Paperwork"
