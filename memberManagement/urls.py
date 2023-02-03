from django.urls import path

from . import views

urlpatterns = [
    path('<str:team_name>', views.IndexView.as_view()),
    path('<str:team_name>/add', views.AddMemberView.as_view()),
]
