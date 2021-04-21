from django.contrib import admin
from equipment.models import System, BrokenEquipmentReport

# Register your models here.
@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    pass


@admin.register(BrokenEquipmentReport)
class BrokenEquipmentReportAdmin(admin.ModelAdmin):
    autocomplete_fields = ["reported_broken_by", "broken_system"]
    readonly_fields = ['date_filed']
    fieldsets = [
        (None, {"fields": ('status',)}),
        ("Report", {"fields": ('date_filed', 'reported_broken_by', 'broken_system',)}),
        (None, {"fields": ('investigation',)})
    ]