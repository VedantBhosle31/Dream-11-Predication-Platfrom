from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("",views.generate_video,name="generate_video"),
]