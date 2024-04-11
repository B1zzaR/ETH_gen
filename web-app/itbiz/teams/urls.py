from django.urls import path
from . import views
urlpatterns = [
    path('', views.teams_home, name="teams_home"),
    path('create', views.create, name="create"),
    path('<int:pk>', views.TeamDetailView.as_view(), name='teams-detail')
]
