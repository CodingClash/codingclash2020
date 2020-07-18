from django.db import models
from django.contrib.auth import get_user_model
import random

class Team(models.Model):

    name = models.CharField(max_length=100)
    rank = models.IntegerField(default=-1)
    elo = models.IntegerField(default=0)
    #secret_key = models.IntegerField(default=0)
    
    #players = []

    @property
    def display_name(self):
        return self.name
        
    def get_latest_submission(self):
        print(self.submission_set)

    def get_displayable(self):
        return {
            "name": self.display_name,
            "rank": self.rank,
            "elo": self.elo,
        }

    def __str__(self):
        return self.name
