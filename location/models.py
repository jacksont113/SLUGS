from django.db import models


# Create your models here.
class Location(models.Model):
    """
    List of common locations for events for Binghamton Sound Stage and Lighting. 
    Only shows the name of the location at the moment and no other information.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
