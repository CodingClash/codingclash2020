import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model


def _code_save_path(instance, filename):
    return os.path.join(instance.user.short_name, f"{uuid.uuid4()}.py")


def _replay_save_path(instance, filename):
    return os.path.join("replays", f"{uuid.uuid4()}.txt")


class Submission(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=500, default="")
    submitted_time = models.DateTimeField(auto_now=True)
    code = models.FileField(upload_to=_code_save_path, default=None)

    def get_name(self):
        return self.name

    def get_user_name(self):
        return self.user.short_name

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
        return f"{self.get_user_name()}: {self.get_submission_name()}"


class Game(models.Model):

    OUTCOME_CHOICES = (
        ("R", "Red"), ("B", "Blue"), ("T", "Tie")
    )

    red = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="red")
    blue = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="blue")
    outcome = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="outcome", blank=True, null=True)
    finished = models.BooleanField(default=False)

    replay = models.FileField(upload_to=_replay_save_path, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def get_red_user(self):
        return self.red.get_user_name()

    def get_blue_user(self):
        return self.blue.get_user_name()

    def get_finished(self):
        return self.finished

    def get_outcome(self):
        return self.outcome

    def get_played_time(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def get_displayable(self, user):
        outcome = "Pending"
        if self.finished:
            if not self.outcome:
                outcome = "Tie"
            elif self.outcome.user == user:
                outcome = "Won"
            else:
                outcome = "Lost"
        return {
            "red": self.get_red_user(),
            "blue": self.get_blue_user(),
            "outcome": outcome,
            "time": self.get_played_time()
        }
