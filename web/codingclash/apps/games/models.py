import os
import uuid
from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from ..teams.models import Team


def _code_save_path(instance, filename):
    print(instance.__dict__)
    prev_submissions = Submission.objects.filter(team=instance.team)
    return os.path.join(str(instance.team.secret), str(len(prev_submissions)) + ".py")
#    return os.path.join(str(instance.team.secret), f"{uuid.uuid4()}.py")


def _replay_save_path(instance, filename):
    return os.path.join("replays", f"{uuid.uuid4()}.txt")


class SubmissionSet(models.Manager):
    def get_team_submissions(self, team):
        return self.get_queryset().filter(team__secret=team.secret)

    def get_team_last_submission(self, team):
        submissions = self.get_team_submissions(team)
        if not submissions:
            return None
        return submissions.order_by('submitted_time').reverse()[0]


class Submission(models.Model):

    objects = SubmissionSet()

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team")
    name = models.CharField(max_length=500, default="")
    submitted_time = models.DateTimeField(auto_now=True)
    code = models.FileField(upload_to=_code_save_path, default=None)

    def get_name(self):
        return self.name

    def get_team_name(self):
        return self.team.name

    def get_submitted_time(self):
        return self.submitted_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_submission_name(self):
        return f'{self.get_name()}: <{self.get_submitted_time()}>'

    def get_code_filename(self):
        return self.code.name

    def delete(self, *args, **kwargs):
        self.code.delete()
        super(Submission, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_team_name()}: {self.get_submission_name()}"


class GameSet(models.Manager):
    def get_user_games(self, user):
        return self.get_queryset().filter(Q(red__team__secret=user.team.secret) |
                                          Q(blue__team__secret=user.team.secret))

    def get_user_displayable(self, user):
        games = self.get_user_games(user).order_by('timestamp')
        games = [game.get_displayable(user.team) for game in games]
        return games

    def get_team_running(self, team):
        return self.get_queryset().filter(finished=False).filter(Q(red__team__secret=team.secret) |
                                                                Q(blue__team__secret=team.secret))


class Game(models.Model):

    objects = GameSet()

    OUTCOME_CHOICES = (
        ("R", "Red"), ("B", "Blue"), ("T", "Tie")
    )

    red = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="red")
    blue = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="blue")
    outcome = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="outcome", blank=True, null=True)
    finished = models.BooleanField(default=False)

    replay = models.FileField(upload_to=_replay_save_path, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def get_red_team(self):
        return self.red.get_team_name()

    def get_blue_team(self):
        return self.blue.get_team_name()

    def get_finished(self):
        return self.finished

    def get_outcome(self):
        return self.outcome

    def get_played_time(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def get_displayable(self, team):
        outcome = "Pending"
        if self.finished:
            if not self.outcome:
                outcome = "Tie"
            elif self.outcome.name == team.name:
                outcome = "Won"
            else:
                outcome = "Lost"
        return {
            "red": self.get_red_team(),
            "blue": self.get_blue_team(),
            "outcome": outcome,
            "time": self.get_played_time(),
            "replay": self.replay.url if self.finished else None
        }


class GameRequest(models.Model):
    my_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="my_team")
    opp_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="opp_team")
    processed = models.BooleanField(default=False)


class SubmissionUpload(forms.Form):
    file = forms.FileField()

