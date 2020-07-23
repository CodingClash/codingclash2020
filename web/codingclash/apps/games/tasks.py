from celery.decorators import task
from celery.utils.log import get_task_logger

from .models import GameRequest, Game

logger = get_task_logger(__name__)


@task(name="play_game")
def play_game(game_request_id):
    game_request = GameRequest.objects.get(id=game_request_id)
    logger.info("Playing a game between {} and {}".format(game_request.my_team.name, game_request.opp_team.name))
    game = Game()


