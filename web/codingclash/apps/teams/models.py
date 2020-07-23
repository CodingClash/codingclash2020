from django.db import models

class Team(models.Model):

    name = models.CharField(max_length=100)
    rank = models.IntegerField(default=-1)
    elo = models.IntegerField(default=1200)
    secret = models.CharField(max_length=16)

    @property
    def display_name(self):
        return self.name

    def get_displayable(self):
        return {
            "name": self.display_name,
            "rank": self.rank,
            "elo": self.elo,
        }

    def __str__(self):
        return self.name
