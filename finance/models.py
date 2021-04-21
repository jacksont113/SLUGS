from django.db import models
from django.contrib.auth.models import Group
import gig.models as gig

# Create your models here.
class Wage(models.Model):
    name = models.CharField(max_length=64)
    hourly_rate = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f'{self.name} - ${self.hourly_rate}/hr'


class Fee(models.Model):
    name = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=512)


class Invoice(models.Model):
    INVOICE_STATUSES = [
        ("E", "Estimate"),
        ("B", "Booked"),
        ("A", "Awaiting Payment"),
        ("C", "Closed"),
    ]
    status = models.CharField(choices=INVOICE_STATUSES, max_length=1)
    gig = models.ForeignKey('gig.Gig', on_delete=models.CASCADE)
    payment_due = models.DateField()
    paid = models.DateField()
    fees = models.ManyToManyField(Fee)


class Shift(models.Model):
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    processed = models.BooleanField(default=False)
    contested = models.BooleanField(default=False)


Group.add_to_class('hourly_rate', models.ForeignKey(Wage, on_delete=models.PROTECT, null=True, blank=True))
