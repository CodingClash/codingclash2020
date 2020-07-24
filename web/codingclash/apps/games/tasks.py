import time
import random
from django.core.files.base import ContentFile

from celery.decorators import task
from celery.utils.log import get_task_logger

from codingclash.celery import app as celery_app

from .models import GameRequest, Game, Submission
from .elo import update_elo
from ..teams.models import Team

MAX_QUEUED = 3
logger = get_task_logger(__name__)


@task(name="play_game")
def play_game(game_request_id):
    game_request = GameRequest.objects.get(id=game_request_id)
    my_team, opp_team = game_request.my_team, game_request.opp_team
    my_queued, opp_queued = len(Game.objects.get_team_running(my_team)), len(Game.objects.get_team_running(opp_team))
    if my_queued >= MAX_QUEUED:
        logger.info("Your team ({}) currently has too many games queued, please wait".format(my_team.name))
        game_request.processed = True
        return
    if opp_queued >= MAX_QUEUED:
        logger.info("The opponent team ({}) currently has too many games queued, please wait".format(opp_team.name))
        game_request.processed = True
        return
    logger.info("Playing a game between {} and {}".format(game_request.my_team.name, game_request.opp_team.name))
    submissions = []
    submissions.append(Submission.objects.get_team_last_submission(game_request.my_team))
    submissions.append(Submission.objects.get_team_last_submission(game_request.opp_team))
    random.shuffle(submissions)
    game = Game(red=submissions[0], blue=submissions[1])
    game.ranked = game_request.ranked
    game.save()
    game_request.processed = True

    # TODO: Actaully run the engine code here
    time.sleep(10)
    winner = my_team if random.random() < 0.4 else opp_team if random.random() < 0.8 else None
    game.outcome = winner
    replay_content = "This be a replay file\nThe winner is: {}".format(winner.name if winner else "Tie")
    game.replay.save(my_team.name + "_" + opp_team.name + "_" + str(random.randint(0, 99999999)) + ".txt", ContentFile(replay_content))
    game.finished = True
    game.save()
    logger.info("The game finished")
    if game.ranked:
        elo1, elo2 = my_team.elo, opp_team.elo
        winner_int = 1 if winner == my_team else -1 if winner == opp_team else 0
        new_elo1, new_elo2 = update_elo(elo1, elo2, winner_int)
        my_team.elo = new_elo1
        opp_team.elo = new_elo2
        my_team.save()
        opp_team.save()


@task(name="update_elos_and_ranks")
def update_elos_and_ranks():
    print("Updating ranks")
    # lookup user by id and send them a message
    teams = Team.objects.all()
    teams = [i for i in teams]
    teams = sorted(teams, key=lambda team: team.elo, reverse=True)
    for i, team in enumerate(teams):
        team.rank = i + 1
        team.display_elo = team.elo
        team.save()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Setting up stuff")
    sender.add_periodic_task(300.0, update_elos_and_ranks.s(), name='Updates elos and ranks every minute')


@celery_app.task
def test(arg):
    print(arg)
