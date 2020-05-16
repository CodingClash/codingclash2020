from django.urls import path
from django.shortcuts import render

from . import views

app_name = "teams"


def default(request):
    return render(request, f"teams/{request.resolver_match.url_name}.html")


urlpatterns = [
]
