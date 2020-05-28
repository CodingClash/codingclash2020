from django.shortcuts import render
from ..teams.models import Team

def leaderboard(request):
    teams = Team.objects.all()
    teams_display = [team.get_displayable() for team in teams]
    teams_display = sorted(teams_display, key=lambda team: team['rank'])
    return render(request, "games/leaderboard.html", {"teams": teams_display})
