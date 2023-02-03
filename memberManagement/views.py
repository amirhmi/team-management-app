from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, CreateView

from memberManagement.forms import MemberForm
from memberManagement.models import Team


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "members"

    def get_queryset(self):
        return Team.objects.get(name=self.kwargs['team_name']).member_set.all()


class AddMemberView(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'add_member.html'

    def get(self, request, *args, **kwargs):
        context = {'form': MemberForm}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        my_data = request.POST
        # do something with your data
        context = {}  # set your context
        return super(TemplateView, self).render_to_response(context)
