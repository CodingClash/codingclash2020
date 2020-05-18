from django.db import models
from django.contrib.auth import get_user_model


class Team(models.Model):

    name = models.CharField(max_length=100)
    rank = models.IntegerField(default=-1)
    elo = models.IntegerField(default=0)
