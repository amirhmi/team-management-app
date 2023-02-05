from django.contrib.auth.models import User
from django.http import HttpResponse

from memberManagement.models import Membership, UserProfile, Team


def is_admin_role(team, user):
    try:
        membership = team.membership_set.get(
            user_profile__user__email=user.email)
    except Membership.DoesNotExist:
        return False
    return membership.role == Membership.Role.ADMIN


def get_or_create_membership_data(form, team):
    if User.objects.filter(username=form.cleaned_data["email"]).exists():
        user = User.objects.get(username=form.cleaned_data["email"])
        user_profile = user.userprofile
    else:
        user = User(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"], username=form.cleaned_data["email"])
        user_profile = UserProfile(user=user, phone_number=form.cleaned_data["phone_number"])

    if Membership.objects.filter(team=team, user_profile=user_profile).exists():
        membership = Membership.objects.get(team=team, user_profile=user_profile)
    else:
        membership = Membership(team=team, user_profile=user_profile, role=form.cleaned_data["role"])

    return user, user_profile, membership


def is_team_admin():
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            try:
                Membership.objects.get(team__name=kwargs['team_name'], user_profile__user=request.user,
                                       role=Membership.Role.ADMIN)
                return function(request, *args, **kwargs)

            except Membership.DoesNotExist:
                return HttpResponse(403)

        return wrapper

    return decorator
