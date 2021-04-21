from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from employee.models import Employee
from crispy_forms.layout import Layout, Div, Field, HTML, Submit


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Employee
        fields = ("email", "first_name", "last_name", "bnum", "phone_number")
        help_texts = {
            'bnum': 'Format: BXXXXXXXXX',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class userCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('email',
                Div(
                    Field('password1', wrapper_class="w-full mr-2"),
                    Field('password2', wrapper_class="w-full ml-2"),
                    css_class="flex w-full"),
                Div(
                    'first_name',
                    'last_name',
                ),
                'phone_number',
                'bnum',
                Submit('submit', 'Submit', css_class="bg-white text-black rounded-sm py-2 px-4"),
                css_class="max-w-5xl my-4 mx-auto",
                ),
        )
