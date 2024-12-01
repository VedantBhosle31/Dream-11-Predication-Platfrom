from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("verify-csv/",views.verify_csv,name="verify_csv"),
    path("get-player-data",views.get_player_data,name="get_player_data"),
    path("get-players",views.get_players,name="get_players"),
    path("get-teams",views.get_teams,name="get_teams"),
    # path("predict",views.predict,name="predict"),
    # path('form', lambda request: render(request, 'predict.html'), name='predict_form'),
]