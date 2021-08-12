from django.contrib import admin
from finance.models import Wage, Shift, Estimate, Fee, OneTimeFee, PayPeriod
from nested_admin import NestedGenericTabularInline


# Register your models here.
@admin.register(Wage)
class WageAdmin(admin.ModelAdmin):
    pass


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    readonly_fields = ["total_time", "cost"]
    exclude = ["content_type", "content_object", "object_id"]
    list_filter = ("processed", "contested")
    pass


class ShiftInlineAdmin(NestedGenericTabularInline):
    readonly_fields = ["total_time", "cost"]
    model = Shift
    extra = 0


class OneTimeFeeInline(admin.StackedInline):
    model = OneTimeFee
    extra = 0


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    inlines = [OneTimeFeeInline]
    list_display = ("__str__", "get_printout_link")
    filter_horizontal = ["fees"]
    autocomplete_fields = ["gig", "billing_contact"]
    readonly_fields = ["subtotal", "fees_amt", "total_amt", "get_printout_link"]
    fieldsets = (
        (
            "Information",
            {
                "fields": [
                    "status",
                    "gig",
                    "billing_contact",
                    "signed_estimate",
                    "notes",
                    "get_printout_link",
                ]
            },
        ),
        ("Billing info", {"fields": ["payment_due", "paid", "fees", "adjustments"]}),
        ("Bill", {"fields": ["subtotal", "fees_amt", "total_amt"]}),
    )


@admin.register(PayPeriod)
class PayPeriodAdmin(admin.ModelAdmin):
    readonly_fields = ["get_summary", "associated_employees", "associated_shifts"]
    exclude = ["shifts"]
