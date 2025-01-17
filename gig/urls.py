from django.urls import path
from . import views

app_name = "gig"
urlpatterns = [
    path("signup/", views.workSignup.as_view(), name="signup"),
    path("list/", views.gigList.as_view(), name="list"),
    path("<gig_id>/", views.gigIndex.as_view(), name="showView"),
    path(
        "<gig_id>/staff_email_template",
        views.generateEmailTemplate.as_view(),
        name="staff_email_template",
    ),
]
