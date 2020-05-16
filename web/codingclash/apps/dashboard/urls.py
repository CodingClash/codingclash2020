from django.urls import path
from django.shortcuts import render

app_name = "dashboard"


def default(request):
    return render(request, f"dashboard/{request.resolver_match.url_name}.html")


urlpatterns = [
    path("about/", default, name="about"),
    path("rules/", default, name="rules"),
    path("schedule/", default, name="schedule"),
]
