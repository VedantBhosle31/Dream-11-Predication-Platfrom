from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("",views.hello,name="hello"),
    path("get_player_points/<int:player_id>/",views.get_player_points,name="get_player_points"),
    path("get_player_radar_chart/<int:player_id>/",views.get_player_radar_chart,name="get_player_radar_chart"),
]