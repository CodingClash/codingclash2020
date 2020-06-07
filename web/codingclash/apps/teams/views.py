import json
from django.shortcuts import render
from django.http import HttpResponse

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
    games = Game.objects.get_user_displayable(request.user)
    teams = [team.name for team in Team.objects.all()]
    return render(request, "teams/history.html", {"games": json.dumps(games), "teams": teams})


def request(request):
    if request.method == "POST" and request.is_ajax():
        json_data = json.loads(request.body)
        if 'opponent' not in json_data:
            return HttpResponse("Failed")
        try:
            opponent = Team.objects.all().get(name=json_data['opponent'])
        except Team.DoesNotExist:
            return HttpResponse("Failed")
        print("Successfully playing game")
        return HttpResponse("OK")
    return HttpResponse("Failed")
