from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("get_predictions",views.get_predictions,name="get_predictions"),
    path('get_all_player_features',views.get_all_player_features,name='get_all_player_features'),
]