from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("verify-csv/",views.verify_csv,name="verify_csv"),
    path("get-player-data",views.get_player_data,name="get_player_data"),
    path("get-player-stats",views.get_player_stats,name="get_player_stats"),
    path("get-players",views.get_players,name="get_players"),
    path("get-teams",views.get_teams,name="get_teams"),
    path("get-team-logos",views.get_team_logos_from_team_names,name="get_team_logos"),
    path('get-player-matchups',views.get_player_matchups,name='get_player_matchups'),
    path('get-player-features',views.get_player_features,name='get_player_features'),
]