from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("predict",views.predict,name="predict"),
    path('form', lambda request: render(request, 'predict.html'), name='predict_form'),
]