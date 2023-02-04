from django.contrib.auth.models import User
from django.shortcuts import render

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from memberManagement.forms import MemberForm
from memberManagement.models import Team, Profile, Membership


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "members"

    def get_queryset(self):
        return Team.objects.get(name=self.kwargs['team_name']).membership_set.all()


class MemberCreateView(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'member_add.html'

    def get(self, request, *args, **kwargs):
        context = {'form': MemberForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        team = Team.objects.get(name=self.kwargs['team_name'])
        user = User(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"], username=form.cleaned_data["email"])
        # check phone number and email uniqueness
        user_profile = Profile(user=user, phone_number=form.cleaned_data["phone_number"])
        membership = Membership(team=team, user=user, role=form.cleaned_data["role"])

        user.save()
        user_profile.save()
        membership.save()

        return HttpResponse(200)


class MemberUpdateView(UpdateView):
    http_method_names = ['get', 'post']
    template_name = 'member_add.html'

    def get(self, request, *args, **kwargs):
        team = Team.objects.get(name=self.kwargs['team_name'])
        user = User.objects.get(pk=self.kwargs['user_id'])
        membership = Membership.objects.get(user=user, team=team)

        form = MemberForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                                   'phone_number': user.profile.phone_number, 'role': membership.role})
        context = {'form': form, "kwargs":kwargs}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        team = Team.objects.get(name=self.kwargs['team_name'])
        user = User.objects.filter(pk=self.kwargs['user_id'])
        membership = Membership.objects.filter(user=user[0], team=team)

        user.update()
        membership.update(role=form.cleaned_data["role"])
        user.update(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"])
        user[0].profile.phone_number = form.cleaned_data["phone_number"]
        return HttpResponse(200)


class MemberDeleteView(DeleteView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        team = Team.objects.get(name=self.kwargs['team_name'])
        user = User.objects.filter(pk=self.kwargs['user_id'])
        membership = Membership.objects.filter(user=user[0], team=team)

        membership.delete()
