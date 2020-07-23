import time
import random
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.files.base import ContentFile

from .models import GameRequest, Game, Submission
from .elo import update_elo

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
    time.sleep(20)
    winner = my_team if random.random() < 0.4 else opp_team if random.random() < 0.8 else None
    game.outcome = winner
    replay_content = "This be a replay file\nThe winner is: {}".format(winner.name if winner else "Tie")
    game.replay.save(my_team.name + "_" + opp_team.name + "_" + str(random.randint(0, 99999999)) + ".txt", ContentFile(replay_content))
    game.finished = True
    game.save()
    logger.info("The game finished")
    if game.ranked:
        elo1, elo2 =
        myteam_won = winner == my_team
        new_elo1, new_elo2 = update_elo()

