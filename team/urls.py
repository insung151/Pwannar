from django.urls import path
from accounts import views

from . import views

app_name = 'team'

urlpatterns = [
    path('create/', views.create_team, name='createteam'),
    path('<str:team_name>/', views.manage_team, name='manage_team'),
    path('<str:team_name>/delete', views.delete_team, name='deleteteam'),
    path('<str:team_name>/startproject', views.start_project, name='startproject'),
    path('<int:pk>/deleteproject/', views.delete_project, name='deleteproject'),
    path('<int:pk>/endproject/', views.end_project, name='endproject'),
]
