from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from memberManagement.forms import MemberForm
from memberManagement.models import Team, UserProfile, Membership


def is_admin_role(team, user):
    try:
        membership = team.membership_set.get(
            user_profile__user__email=user.email)
    except Membership.DoesNotExist:
        return False
    return membership.role == Membership.Role.ADMIN


class IndexView(ListView):
    template_name = "member_list.html"
    context_object_name = "members"

    def get(self, request, *args, **kwargs):
        team = Team.objects.get(name=self.kwargs['team_name'])
        context = {'members': team.membership_set.all(),
                   'is_admin': is_admin_role(team, request.user), "kwargs": kwargs}
        return render(request, self.template_name, context)


class MemberCreateView(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'member_page.html'

    def get(self, request, *args, **kwargs):
        context = {'form': MemberForm, 'is_add': True}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        print(form)
        if not form.is_valid():
            print(form.errors)
            context = {'form': form}
            return render(request, self.template_name, context)

        team = Team.objects.get(name=self.kwargs['team_name'])
        user = User(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"], username=form.cleaned_data["email"])
        # check phone number and email uniqueness
        user_profile = UserProfile(user=user, phone_number=form.cleaned_data["phone_number"])
        membership = Membership(team=team, user_profile=user_profile, role=form.cleaned_data["role"])

        user.save()
        user_profile.save()
        membership.save()

        return HttpResponse(200)


class MemberUpdateView(UpdateView):
    http_method_names = ['get', 'post']
    template_name = 'member_page.html'

    def get(self, request, *args, **kwargs):
        team = Team.objects.get(name=self.kwargs['team_name'])
        user_profile = UserProfile.objects.get(pk=self.kwargs['user_id'])
        membership = Membership.objects.get(user_profile=user_profile, team=team)
        user = user_profile.user

        form = MemberForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                                   'phone_number': user_profile.phone_number, 'role': membership.role})
        context = {'form': form, "kwargs": kwargs, 'is_add': False}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        team = Team.objects.get(name=self.kwargs['team_name'])
        user_profile = UserProfile.objects.filter(pk=self.kwargs['user_id'])
        membership = Membership.objects.filter(user=user_profile[0], team=team)

        user_profile.update()
        membership.update(role=form.cleaned_data["role"])
        user_profile.update(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"],
                            email=form.cleaned_data["email"])
        user_profile[0].user_profile.phone_number = form.cleaned_data["phone_number"]
        return HttpResponse(200)


class MemberDeleteView(DeleteView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        team = Team.objects.get(name=self.kwargs['team_name'])
        user_profile = UserProfile.objects.filter(pk=self.kwargs['user_id'])
        membership = Membership.objects.filter(user_profile=user_profile[0], team=team)

        membership.delete()
        return redirect(reverse('member_list', kwargs={"team_name": team.name}))
