import json
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from players.utils.player_service import get_player_stats
# from services.player_service import get_player_stats
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

import json


# Create your views here.
PLAYER_NAMES_PATH = "players/utils/player_names.csv"
TEAM_NAMES_PATH = "players/utils/team_details.csv"
PLAYER_DATA_PATH = "players/utils/player_datails.json"


def home(request):
    return HttpResponse("hello world!")


@csrf_exempt
@parser_classes([MultiPartParser, FormParser])
def verify_csv(request):
    if request.method == "POST":
        print("request", request.body)
        print("request", request.FILES)
        from .utils.validators import validate_uploaded_csv

        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            result = validate_uploaded_csv(file, PLAYER_NAMES_PATH, TEAM_NAMES_PATH)
            errors = result["errors"]
            logos = result["team_logos"]
            if errors:
                return JsonResponse({"status": "error", "errors": errors}, status=400)
            return JsonResponse(
                {"status": "success", "message": "File is valid.", "team_logos": logos}
            )
        return JsonResponse(
            {
                "status": "error",
                "message": "No file provided or invalid request method.",
            },
            status=400,
        )


@csrf_exempt
def get_players(request):
    if request.method == "GET":
        user_input = request.GET.get("user_input")
        # If user_input is greater than 3 characters, search for player names
        if len(user_input) > 3:
            player_names = pd.read_csv(PLAYER_NAMES_PATH)
            player_names = player_names[
                player_names["cricsheet_name"].str.contains(user_input, case=False)
            ]
            player_names = player_names["cricsheet_name"].tolist()
            return JsonResponse({"player_names": player_names})


@csrf_exempt
def get_player_data(request):
    if request.method == "GET":
        body = json.loads(request.body)
        player_name = body['name']
        date = body['date']
        model = body['model']
        stats = get_player_stats(player_name,date,model)
        return JsonResponse({'stats':stats})
        
def get_teams():
    pass

def get_team_logos_from_team_names():
    pass

def get_player_matchups():
    pass

def get_player_features():
    pass
