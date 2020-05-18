import json
from django.shortcuts import render

from ..games.models import *


def info(request):
    return render(request, "teams/info.html")


def submission(request):
    return render(request, "teams/submission.html")


def history(request):
    games = Game.objects.filter(red__user=request.user) | Game.objects.filter(blue__user=request.user)
    games_display = [game.get_displayable(request.user) for game in games]
    games_display = sorted(games_display, key=lambda game: game['time'], reverse=True)
    return render(request, "teams/history.html", {"games": json.dumps(games_display)})

