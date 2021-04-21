from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from employee.forms import userCreationForm


# Create your views here.
class userSignup(FormView):
    form_class = userCreationForm
    success_url = "/employee/onboard/success"
    template_name = "employee/signup.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class userSignupComplete(TemplateView):
    template_name = "employee/signup_complete.html"