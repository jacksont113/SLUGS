from django.contrib import admin
from finance.models import Wage


# Register your models here.
@admin.register(Wage)
class WageAdmin(admin.ModelAdmin):
    pass
