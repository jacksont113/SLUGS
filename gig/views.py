from SLUGS.templatetags.grouping import has_group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from dev_utils.views import MultipleFormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from SLUGS.views import SLUGSMixin, isAdminMixin
from gig.models import Gig, Job, JobInterest
from employee.models import Employee
from datetime import datetime
from django.db.models import F, DateTimeField, ExpressionWrapper
from django.utils import timezone


from finance.forms import ShiftFormSet
from gig.forms import sendStaffingEmailForm, shiftFormHelper, engineerNotesForm, StaffShowForm
from finance.models import Shift, Estimate
from utils.models import signupStatus


# Create your views here.
class gigIndex(SLUGSMixin, MultipleFormView):
    template_name = "gig/gig.html"
    form_classes = {}

    def post_valid_reject(self, context):
        return self.get_context_data(context)

    def get_context_data(self, ctext=False, **kwargs):
        context = super().get_context_data(**kwargs)
        for form in context["forms"]:
            if form != "show_notes":
                if form in context["job_forms"]:
                    context["forms"][form] = {
                        "form": context["forms"][form],
                        "employee": context["job_forms"][form].employee,
                    }
        return context

    def dispatch(self, request, *args, **kwargs):
        self.form_classes = {
            "show_notes": {
                "form": engineerNotesForm,
            }
        }
        jobs = {}
        self.added_context["helper"] = shiftFormHelper()
        self.added_context["gig"] = Gig.objects.get(pk=kwargs["gig_id"])
        if not self.added_context["gig"].published:
            raise PermissionDenied()
        try:
            self.added_context["my_job"] = (
                Job.objects.get(employee=request.user, gig=self.added_context["gig"])
                if request.user.is_authenticated
                else ""
            )
        except Exception:
            self.added_context["my_job"] = False
        for job in self.added_context["gig"].job_set.all():
            jobs[f"job_form_{job.id}"] = job
            self.form_classes[f"job_form_{job.id}"] = {
                "form": ShiftFormSet,
                "kwargs": {
                    "queryset": Shift.objects.filter(
                        object_id=job.id,
                        content_type_id=ContentType.objects.get(model="job").id,
                    )
                },
            }
        self.form_classes["show_notes"]["instance"] = self.added_context["gig"]
        self.added_context["job_forms"] = jobs
        return super().dispatch(request, *args, **kwargs)

    def process_forms(self, form_instances):
        for form in form_instances["forms"]:
            if form == "show_notes":
                form_instances["forms"][form].save()
            else:
                for shift in form_instances["forms"][form].forms:
                    if "DELETE" in shift.changed_data:
                        shift.save()
                        continue
                    if (
                        shift.instance.time_in is not None
                        and shift.instance.time_out is not None
                    ):
                        shift.instance.object_id = self.added_context["job_forms"][
                            form
                        ].id
                        shift.instance.content_type_id = ContentType.objects.get(
                            model="job"
                        ).id
                        shift.save()
                form_instances["forms"][form].save()
        messages.add_message(self.request, messages.SUCCESS, "Day of Show updated")
        return self.render_to_response(self.get_context_data())


class workSignup(SLUGSMixin, TemplateView):
    template_name = "gig/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if not signupStatus.objects.all().first().is_open or has_group(
            request.user, "Cannot Work"
        ):
            raise PermissionDenied()
        self.added_context["gigs"] = list(
            set(
                Gig.objects.filter(
                    start__gte=timezone.now(),
                    available_for_signup__lte=timezone.now(),
                    job__employee=None,
                    published=True,
                ).order_by("-start")
            )
        )
        return super().dispatch(request, *args, **kwargs)


class gigList(SLUGSMixin, TemplateView):
    template_name = "gig/list.html"

    def dispatch(self, request, *args, **kwargs):
        self.added_context["gigs"] = Gig.objects.filter(published=True).order_by(
            "-start"
        )[:150]
        self.added_context["signup_open"] = signupStatus.objects.first().is_open
        return super().dispatch(request, *args, **kwargs)


class staffShow(SLUGSMixin, MultipleFormView):
    template_name = "gig/staff.html"

    def dispatch(self, request, *args, **kwargs):
        self.added_context["gig"] = Gig.objects.get(pk=kwargs["object_id"])
        self.added_context["unfilled_positions"] = [
            [job, []]
            for job in Job.objects.filter(gig=self.added_context["gig"], employee=None)
        ]
        for position in self.added_context["unfilled_positions"]:
            position[1] = Employee.objects.filter(
                pk__in=JobInterest.objects.filter(job=position[0]).values_list(
                    "employee", flat=True
                )
            )
            self.form_classes[f"job_{position[0].pk}"] = {
                "form": StaffShowForm,
                "instance": position[0],
                "kwargs": {"interested_employees": position[1]},
            }
        return super().dispatch(request, *args, **kwargs)

    def process_forms(self, form_instances):
        for form in form_instances["forms"]:
            f = form_instances["forms"][form]
            if Job.objects.get(pk=f.instance.pk).employee is None:
                if f.instance.employee is not None:
                    if not f.instance.employee.groups.filter(
                        name=f.instance.position
                    ).exists():
                        f.instance.is_test = True
                f.save()
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    f'Job "{f.instance.get_department_display()} - {f.instance.position}" not overridden as it was filled by another manager before you submitted your staffing. (RACE CONDITION)',
                )
        messages.add_message(
            self.request, messages.SUCCESS, "Selected employees staffed"
        )
        return redirect("admin:gig_gig_change", object_id=self.added_context["gig"].pk)


class SendStaffingEmail(SLUGSMixin, FormView):
    template_name = "gig/send_email.html"
    form_class = sendStaffingEmailForm

    def dispatch(self, request, *args, **kwargs):
        self.added_context["gig"] = Gig.objects.get(pk=kwargs["object_id"])
        self.added_context["request"] = request
        template = get_template("gig/components/staff_email_template.html")
        self.added_context["email_template"] = template.render(self.added_context)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employees'] = self.added_context['gig'].job_set.exclude(employee=None).values_list('employee__preferred_name', 'employee__first_name', 'employee__last_name', 'employee__pk').distinct()
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["employees_working"] = list(self.added_context['gig'].job_set.values_list('employee__pk', flat=True).distinct())
        return initial

    def form_valid(self, form):
        recipient_list = [
            Employee.objects.get(pk=emp_id).email for emp_id in form.cleaned_data["employees_working"]
        ]
        email = EmailMessage(
            f"You've been staffed for {self.added_context['gig'].name}",
            self.added_context["email_template"],
            "bssl.slugs@binghamtonsa.org",
            [],
            recipient_list,
            reply_to=["bssl@binghamtonsa.org"],
        )
        email.content_subtype = "html"
        email.send()
        messages.add_message(
            self.request, messages.SUCCESS, "Email sent to employees working this show"
        )
        return redirect("admin:gig_gig_change", object_id=self.added_context["gig"].pk)


@method_decorator(xframe_options_exempt, name="dispatch")
class generateEmailTemplate(SLUGSMixin, TemplateView):
    template_name = "gig/components/staff_email_template.html"

    def dispatch(self, request, *args, **kwargs):
        self.added_context["gig"] = Gig.objects.get(pk=kwargs["gig_id"])
        return super().dispatch(request, *args, **kwargs)

class BookingOverview(SLUGSMixin, isAdminMixin, TemplateView):
    template_name = "gig/booking.html"

    def dispatch(self, request, *args, **kwargs):
        self.added_context["outstanding_bookings"] = Estimate.objects.filter(gig__start__gte=datetime.now(), status__in=["E", "L"]).order_by("gig__start").annotate(three_weeks_prior=ExpressionWrapper(F('gig__start')-timezone.timedelta(weeks=3), output_field=DateTimeField()))
        self.added_context["gig_wo_estimate"] = Gig.objects.filter(estimate=None, start__gte=datetime.now())
        return super().dispatch(request, *args, **kwargs)
