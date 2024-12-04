from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("",views.generate_video,name="generate_video"),
    path("generate_pptx_images_and_audio",views.generate_pptx_images_and_audio,name="generate_pptx_images_and_audio")
]