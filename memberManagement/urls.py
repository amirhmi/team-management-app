from django.urls import path

from . import views

urlpatterns = [
    path('<str:team_name>', views.list, name='index'),
]