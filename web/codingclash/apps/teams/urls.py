from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import Group
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

import random
from . import models
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
            try:
                tm=Team.objects.get(pk=int(secret))
                user = get_user_model()

                #tm.players.append(user)

                user.team = tm

                #user.team.save()

            except:
                return redirect('/join')
            return redirect('/')
    else:
        form = JoinForm()
    return render(request, f"teams/join.html", {'form': form})


def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            k = int(''.join(random.choice('0123456789') for i in range(16)))
            tm = models.Team(name=name, pk=k)
            user = get_user_model()

            #tm.players.append(user)

            user.team = tm

            #user.team.save()

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
    path("request/", views.request, name="request")
]
