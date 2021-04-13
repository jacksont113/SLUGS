from django_unicorn.components import UnicornView
from utils.models import signupStatus


class SignupstatusView(UnicornView):
    signup = signupStatus.objects.first()

    def toggle(self):
        self.signup.is_open = False if self.signup.is_open else True
        self.signup.save()
