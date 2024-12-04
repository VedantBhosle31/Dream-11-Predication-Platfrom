from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path("explain-graph/",views.explain_graph,name="explain_graph"),
    path("describe-player/", views.describe_player,name="describe_player"),
    path("get-ai-auio/", views.get_ai_audio,name="get_audio")

]