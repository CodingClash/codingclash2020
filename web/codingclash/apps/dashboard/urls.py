from django.urls import path
from django.shortcuts import render

app_name = "dashboard"


def default(request):
    return render(request, f"dashboard/{request.resolver_match.url_name}.html")


urlpatterns = [
    path("contact/", default, name="contact"),
    path("rules/", default, name="rules"),
    path("schedule/", default, name="schedule"),
]
