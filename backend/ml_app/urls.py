from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("get_predictions",views.get_predictions,name="get_predictions"),
    # path('form', lambda request: render(request, 'predict.html'), name='predict_form'),
]