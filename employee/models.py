import os
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

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
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bnum = models.CharField(null=True, max_length=12, verbose_name="B Number")
    phone_number = PhoneNumberField(null=True)
    is_grad_student = models.BooleanField(default=False)
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


class OfficeHours(models.Model):
    position = models.ForeignKey(
        Group, default="Manager", to_field='name', on_delete=models.PROTECT
    )
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    shifts = GenericRelation("finance.Shift")

    class Meta:
        verbose_name_plural = "Office Hours"

    def __str__(self):
        return "Office Hours"


class Paperwork(models.Model):
    form_name = models.CharField(max_length=256)
    form_pdf = models.FileField(upload_to="forms/")
    uploaded = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form_name} {self.edited.year}"

    class Meta:
        verbose_name = "Paperwork"
        verbose_name_plural = "Paperwork"


class PaperworkForm(models.Model):
    def user_dir_path(instance, filename):
        fileName, fileExtension = os.path.splitext(filename)
        return f"uploads/{instance.employee.bnum}/{instance.employee.bnum}_{instance.employee.first_name[0].upper()}{instance.employee.last_name}_{str(instance.form)}{fileExtension}" # noqa

    form = models.ForeignKey("employee.Paperwork", on_delete=models.PROTECT)
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    pdf = models.FileField(upload_to=user_dir_path, blank=True, null=True)
    uploaded = models.DateTimeField(blank=True, null=True)
    requested = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.form}"
