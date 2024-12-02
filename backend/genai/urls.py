from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("explain-graph/",views.explain_graph,name="explain_graph"),

]