from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("verify-csv/",views.verify_csv,name="verify_csv"),
    path("get-player-data/<str:player_id>",views.get_player_data,name="get_player_data"),
    # path("predict",views.predict,name="predict"),
    # path('form', lambda request: render(request, 'predict.html'), name='predict_form'),
]