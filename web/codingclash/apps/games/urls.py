from django.urls import path
from django.shortcuts import render

from . import views

app_name = "games"


def default(request):
    return render(request, f"games/{request.resolver_match.url_name}.html")


urlpatterns = [
    path("about/", default, name="about"),
    path("rules/", default, name="rules"),
    path("schedule/", default, name="schedule"),
    path("visualizer/", default, name="visualizer"),
    path("leaderboard/", default, name="leaderboard"),
]
