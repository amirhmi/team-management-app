from django.urls import path

from . import views

urlpatterns = [
    path('<str:team_name>/', views.IndexView.as_view(), name="member_list"),
    path('<str:team_name>/add/', views.MemberCreateView.as_view(), name="member_add"),
    path('<str:team_name>/<int:user_id>/', views.MemberUpdateView.as_view(), name="member_edit"),
    path('<str:team_name>/<int:user_id>/delete/', views.MemberDeleteView.as_view(), name="member_delete"),
]
