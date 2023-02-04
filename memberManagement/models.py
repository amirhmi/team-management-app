from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


#change to Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Role(models.TextChoices):
        ADMIN = 'AD', _('Admin')
        REGULAR = 'RE', _('Regular')

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.REGULAR,
    )
