import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from .models import *

def info(request):
    return render(request, "teams/info.html")


def submission(request):
    return render(request, "teams/submission.html")


def history(request):
    games = Game.objects.filter(red__user=request.user) | Game.objects.filter(blue__user=request.user)
    games_display = [game.get_displayable(request.user) for game in games]
    games_display = sorted(games_display, key=lambda game: game['time'], reverse=True)
    return render(request, "teams/history.html", {"games": json.dumps(games_display)})

