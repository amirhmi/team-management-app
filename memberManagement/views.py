from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from memberManagement.forms import MemberForm
from memberManagement.models import Team, UserProfile, Membership
from memberManagement.utils import is_admin_role, get_or_create_membership_data, is_team_admin


class IndexView(ListView):
    template_name = "member_list.html"
    context_object_name = "members"

    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, name=self.kwargs['team_name'])
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
        if not form.is_valid():
            context = {'form': form, 'error_message': form.errors}
            return render(request, self.template_name, context)

        team = get_object_or_404(Team, name=self.kwargs['team_name'])
        user, user_profile, membership = get_or_create_membership_data(form, team)

        user.save()
        user_profile.save()
        membership.save()

        return redirect(reverse('member_list', kwargs={"team_name": team.name}))


class MemberUpdateView(UpdateView):
    http_method_names = ['get', 'post']
    template_name = 'member_page.html'

    @method_decorator(is_team_admin())
    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, name=self.kwargs['team_name'])
        user_profile = UserProfile.objects.get(pk=self.kwargs['user_id'])
        membership = Membership.objects.get(user_profile=user_profile, team=team)
        user = user_profile.user

        form = MemberForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                                   'phone_number': user_profile.phone_number, 'role': membership.role})
        context = {'form': form, "kwargs": kwargs, 'is_add': False}
        return render(request, self.template_name, context)

    @method_decorator(is_team_admin())
    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if not form.is_valid():
            context = {'form': form, 'error_message': form.errors}
            return render(request, self.template_name, context)

        team = get_object_or_404(Team, name=self.kwargs['team_name'])
        user = User.objects.filter(userprofile__pk=self.kwargs['user_id'])
        user_profile = UserProfile.objects.filter(pk=self.kwargs['user_id'])
        membership = Membership.objects.filter(user_profile=user_profile[0], team=team)

        membership.update(role=form.cleaned_data["role"])
        user.update(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"])
        user_profile.update(phone_number=form.cleaned_data["phone_number"])
        return redirect(reverse('member_list', kwargs={"team_name": team.name}))


class MemberDeleteView(DeleteView):
    http_method_names = ['post']

    @method_decorator(is_team_admin())
    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, name=self.kwargs['team_name'])
        user_profile = UserProfile.objects.filter(pk=self.kwargs['user_id'])
        membership = Membership.objects.filter(user_profile=user_profile[0], team=team)

        membership.delete()
        return redirect(reverse('member_list', kwargs={"team_name": team.name}))
