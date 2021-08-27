from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from utils.models import Notification, signupStatus
from gig.models import Gig, Job


def get_closest_to_dt(qs, dt):
    greater = qs.filter(dt__gte=dt).order_by("dt").first()
    less = qs.filter(dt__lte=dt).order_by("-dt").first()

    if greater and less:
        return greater if abs(greater.dt - dt) < abs(less.dt - dt) else less
    else:
        return greater or less


class SLUGSMixin:
    added_context = {}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("%s?next=%s" % (reverse("login"), request.path))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.added_context)
        return context


class index(SLUGSMixin, TemplateView):
    template_name = "SLUGS/index.html"

    def dispatch(self, request, *args, **kwargs):
        self.added_context["notifications"] = Notification.objects.all()
        self.added_context["signup_open"] = signupStatus.objects.first().is_open
        self.added_context["jobs"] = (
            (
                Job.objects.all()
                .filter(employee=request.user)
                .select_related("gig")
                .order_by("-gig__start")[:5]
            )
            if request.user.is_authenticated
            else None
        )
        if request.user.is_authenticated:
            next_gig_id = (
                Job.objects.filter(employee=request.user)
                .filter(gig__end__gte=timezone.now())
                .values(
                    "gig__id",
                )
                .order_by("gig__end")[:1]
            )
            self.added_context["next_gig"] = (
                Gig.objects.get(pk=next_gig_id[0]["gig__id"])
                if (len(next_gig_id) > 0)
                else None
            )
        return super().dispatch(request, *args, **kwargs)
