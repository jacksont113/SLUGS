from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Organization(models.Model):
    name = models.CharField(max_length=200)
    SA_account_num = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class OrgContact(models.Model):
    name = models.CharField(max_length=200)
    linked_org = models.ForeignKey(Organization, models.PROTECT)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.linked_org}"
