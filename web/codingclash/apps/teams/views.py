import json
from django.shortcuts import render

from ..games.models import *



def info(request):
    return render(request, "teams/info.html")


def create_submission(request):
    print(request.FILES)
    for filename, file in request.FILES.items():
        file = request.FILES[filename]
    team = request.user.team
    submission = Submission(team=team, name=file.name, code=file)
    submission.save()


def submission(request):
    if request.method == 'POST':
        form = SubmissionUpload(request.POST, request.FILES)
        print(request.user)
        if form.is_valid():
            create_submission(request)
            return history(request)
    else:
        form = SubmissionUpload()
    return render(request, "teams/submission.html", {'form': form})


def history(request):
    games = Game.objects.filter(red__user=request.user) | Game.objects.filter(blue__user=request.user)
    games_display = [game.get_displayable(request.user) for game in games]
    games_display = sorted(games_display, key=lambda game: game['time'], reverse=True)
    return render(request, "teams/history.html", {"games": json.dumps(games_display)})

