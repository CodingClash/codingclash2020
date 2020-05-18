from django.db import models
from django.contrib.auth import get_user_model


class Team(models.Model):

    name = models.CharField(max_length=100)
    rank = models.IntegerField(default=-1)
    elo = models.IntegerField(default=0)

    @property
    def display_name(self):
        return self.name

    def __str__(self):
        return self.name
