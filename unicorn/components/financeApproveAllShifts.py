from django_unicorn.components import UnicornView
from finance.models import Shift


class FinanceapproveallshiftsView(UnicornView):
    shifts = None
    allAccepted = False

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.shifts = kwargs["shiftset"]
        self.allAccepted = kwargs["shiftset"].filter(processed=False).count() == 0

    def acceptAll(self):
        for shift in self.shifts:
            s = Shift.objects.get(pk=shift.pk)
            s.processed = True if not self.allAccepted else False
            s.save()
        self.allAccepted = True if self.allAccepted is False else False
