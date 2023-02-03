from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def list(request, team_name):
    return HttpResponse(f"Hello, world. {team_name}")

