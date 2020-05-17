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

"""
def replay(request):
    if request.method == "POST":
        form = PDFForm(request.POST)
        if form.is_valid():
            buffer = io.BytesIO()
            cd = form.cleaned_data
            create_pdf(buffer, cd['board'], cd['solved'], cd['height'], cd['clues']['across'], cd['clues']['down'], cd['title'], cd['solution']).save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='puzzle.pdf')
        else:
            for err in form.errors.as_data()["__all__"]:
                messages.error(request, err.message, extra_tags="danger")
    return redirect("codingclash:history")
"""