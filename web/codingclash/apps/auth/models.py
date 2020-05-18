import logging

from django.db import models
from django.contrib.auth.models import AbstractUser
from ..teams.models import Team

logger = logging.getLogger(__name__)


class User(AbstractUser):
    ACCESS_TYPES = (("none", "None"), ("view", "View"), ("edit", "Edit"))

    id = models.AutoField(primary_key=True)

    access_type = models.CharField(max_length=10, choices=ACCESS_TYPES, default="none")

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="users", blank=True, null=True)

    @property
    def has_management_permission(self) -> bool:
        return self.access_type == "edit" or self.is_staff or self.is_superuser

    @property
    def short_name(self):
        return self.username

    def get_social_auth(self):
        return self.social_auth.get(provider="ion")

    def __str__(self):
        return self.short_name
