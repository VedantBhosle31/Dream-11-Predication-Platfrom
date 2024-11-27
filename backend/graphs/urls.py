from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("",views.hello,name="hello"),
    path("get_player_points",views.get_player_points,name="get_player_points"),
]