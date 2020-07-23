from django.urls import path
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

import random
from .models import Team
from . import views

app_name = "teams"
class JoinForm(forms.Form):
    secret = forms.CharField(label="Secret Key", max_length = 32)

class CreateForm(forms.Form):
    name = forms.CharField(label="Team Name", max_length = 32)

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            secret = form.cleaned_data.get('secret')
            teams = Team.objects.filter(secret=secret)
            assert(len(teams) <= 1)
            if teams:
                user = request.user
                user.team = teams[0]
                user.save()
                return redirect('/')
            messages.error(request, "Error, that secret key is not recognized")
            return redirect('/join')
    else:
        form = JoinForm()
    return render(request, f"teams/join.html", {'form': form})


def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if Team.objects.filter(name=name):
                messages.error(request, "Error, that name is already chosen")
            else:
                k = ''.join(random.choice('0123456789') for i in range(16))
                while Team.objects.filter(secret=k):
                    k = ''.join(random.choice('0123456789') for i in range(16))

                team = Team(name=name, secret=k)
                user = request.user
                team.save()
                user.team = team
                user.save()
                return redirect('/info')
    else:
        form = CreateForm()
    return render(request, f"teams/create.html", {'form': form})

def default(request):
    return render(request, f"teams/{request.resolver_match.url_name}.html")


urlpatterns = [
    path("join/", join, name="join"),
    path("create/", create, name="create"),
    path("info/", views.info, name="info"),
    path("submission/", views.submission, name="submission"),
    path("history/", views.history, name="history"),
    path("game_request/", views.game_request, name="game_request")
]
