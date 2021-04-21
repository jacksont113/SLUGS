from django.urls import path
from . import views

app_name = "employee"
urlpatterns = [
    path("onboard", views.userSignup.as_view(), name="signup"),
    path("onboard/success", views.userSignupComplete.as_view(), name="signup_complete"),
]
