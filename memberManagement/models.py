from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(max_length=100)


class Member(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Role(models.TextChoices):
        ADMIN = 'AD', _('Admin')
        REGULAR = 'RE', _('Regular')

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.REGULAR,
    )
