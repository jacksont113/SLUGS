from django_unicorn.components import UnicornView
import django.utils.timezone as timezone
from gig.models import Job


class GigshiftView(UnicornView):
    job = None
    reload = False

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.job = Job.objects.get(pk=kwargs["job"].pk)

    def clock_in(self):
        self.job.shifts.create(time_in=timezone.now())
        self.job.save()

    def clock_out(self):
        shift = self.job.shifts.order_by("time_out").first()
        shift.time_out = timezone.now()
        shift.save()
        self.job.save()
        self.reload = True
