from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ", ".join(groups)

    group.short_description = "Groups"

    list_display = ("__str__", "group", "is_active", "is_staff", "is_superuser")
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups"
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        else:
            # modify these to suit the fields you want your
            # is_staff user to be able to edit
            perm_fields = ("is_active", "is_staff", "groups")

        return [
            (None, {"fields": ("email", "password")}),
            (
                "Personal info",
                {"fields": ("first_name", "last_name", "phone_number", "bnum")},
            ),
            ("Permissions", {"fields": perm_fields}),
        ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "bnum",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name", "bnum", "groups")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
