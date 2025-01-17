from django.db import models
from gig.models import DEPARTMENTS
import employee.models as employee


# Create your models here.
class System(models.Model):
    """
    List of all Binghamton Sound Stage and Lighting systems with name, description, department, and price per hour.
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1024, blank=True, null=True)
    department = models.CharField(max_length=1, choices=DEPARTMENTS)
    base_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    price_per_hour = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return self.department + " - " + self.name


class SystemAddon(models.Model):
    """
    List of all recorded BSSL Addons. Each addon includes the name of the addon, description,
    department, base price, price per hour/price per hour for load in and out (if applicable),  and included equipment with quantity.
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1024, blank=True, null=True)
    department = models.CharField(max_length=1, choices=DEPARTMENTS)
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    price_per_hour_for_duration_of_gig = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00
    )
    price_per_hour_for_load_in_out_ONLY = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00
    )

    def __str__(self):
        return self.name


class BrokenEquipmentReport(models.Model):
    """
    Lists all submitted broken equipment reports in BSSL. 
    The format of each report is STATUS – SOUND OR LIGHTING – SYSTEM (ex A,Large,Uplighting). 
    This model gives you access to edit the status, the person who reported the issue, what system is broken, and notes on what is broken. 
    The page also includes an investigation note box to give information on how the problem was solved. Reports can also be added from this model. 
    """
    CASE_TYPES = [
        ("U", "Unread"),
        ("A", "Acknowledged"),
        ("W", "WIP"),
        ("B", "Blocked"),
        ("C", "Closed"),
    ]
    broken_system = models.ForeignKey(System, on_delete=models.CASCADE)
    date_filed = models.DateTimeField(auto_now_add=True)
    reported_broken_by = models.ForeignKey(employee.Employee, models.PROTECT, null=True)
    notes = models.TextField()
    investigation = models.TextField(null=True, blank=True)
    status = models.CharField(choices=CASE_TYPES, max_length=1, null=True)

    def __str__(self):
        return self.status + " - " + str(self.broken_system)
