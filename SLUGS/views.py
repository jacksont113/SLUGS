from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from utils.models import Notification, signupStatus


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
        return super().dispatch(request, *args, **kwargs)
