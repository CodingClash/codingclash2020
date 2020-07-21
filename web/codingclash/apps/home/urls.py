from django.urls import path
from django.shortcuts import render

from . import views

app_name = "home"


def default(request):
    return render(request, f"home/{request.resolver_match.url_name}.html")


urlpatterns = [
    path("", default, name="home")
]
