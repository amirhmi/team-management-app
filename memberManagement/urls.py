from django.urls import path

from . import views

urlpatterns = [
    path('<str:team_name>/', views.IndexView.as_view()),
    path('<str:team_name>/add/', views.MemberCreateView.as_view()),
    path('<str:team_name>/<int:user_id>/', views.MemberUpdateView.as_view()),
    path('<str:team_name>/<int:user_id>/delete/', views.MemberDeleteView.as_view(), name="member_delete"),
]
