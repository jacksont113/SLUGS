from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from fieldsets_with_inlines import FieldsetsInlineMixin
from .models import SystemInstance, Gig, Job, LoadIn


class JobSubInline(NestedTabularInline):
    autocomplete_fields = ['employee']
    model = Job
    exclude = ['gig']
    extra = 0


class JobInline(NestedTabularInline):
    autocomplete_fields = ['employee']
    model = Job
    extra = 0


class SystemInline(NestedStackedInline):
    autocomplete_fields = ['system']
    model = SystemInstance
    inlines = (JobSubInline,)
    extra = 1


class LoadInInline(NestedTabularInline):
    model = LoadIn
    extra = 0


@admin.register(Gig)
class GigAdmin(NestedModelAdmin):
    inlines = (SystemInline, JobInline, LoadInInline)
    autocomplete_fields = ['org', 'contact', 'location']
    fieldsets = [
        ("Event Information", {"fields": ('name', 'start', 'end', 'org', 'contact', 'location', 'notes',)}),
        ("Day of Show Info", {"fields": ('day_of_show_notes',)}),
        (None, {"fields": ('archived',)}),
    ]

    # def save_formset(self, request, form, formset, change):
    #     for form in formset.forms:
    #         if 'nested_formsets' in form:
    #             for job_form in form.nested_formsets:
    #                 for project_form in job_form:
    #                     project_form.instance.gig = form.instance.id

        # super(GigAdmin, self).save_formset(request, form, formset, change)
