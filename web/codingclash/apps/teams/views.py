import json
from django.shortcuts import render, redirect
from django.http import HttpResponse

from ..games.models import *
from ..games.tasks import play_game

class LeaveForm(forms.Form):
    pass

def info(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            request.user.team = None
            request.user.save()
            return redirect('/join')
    else:
        return render(request, "teams/info.html", {"secret": request.user.team.secret})


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
    if request.method == "POST":
        opp_team = None
        try:
            json_data = json.loads(request.body)
            opp_team_name = json_data['opponent']
            assert(request.user.team.name != opp_team_name)
            opp_team = Team.objects.all().get(name=opp_team_name)
        except json.decoder.JSONDecodeError:
            print("Incorrect request json format")
        except KeyError:
            print("Opponent field not found in request body")
        except Team.DoesNotExist:
            print("Opponent team not found")
        except AssertionError:
            print("Can't play against yourself")

        if not opp_team:
            return HttpResponse("Failed")
        game_request = GameRequest(my_team=request.user.team, opp_team=opp_team)
        game_request.save()
        print("Successfully starting game")
        play_game.delay(game_request.id)
        return HttpResponse("OK")
    # Incorrect request format
    return HttpResponse("Failed")

