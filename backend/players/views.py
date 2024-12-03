# import json
# from django.shortcuts import render
# import pandas as pd
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# from players.utils.player_service import get_player_stats
# # from services.player_service import get_player_stats
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.decorators import parser_classes

# import json


# # Create your views here.
# PLAYER_NAMES_PATH = "players/utils/player_names.csv"
# TEAM_NAMES_PATH = "players/utils/team_details.csv"
# PLAYER_DATA_PATH = "players/utils/player_datails.json"


# def home(request):
#     return HttpResponse("hello world!")


# @csrf_exempt
# @parser_classes([MultiPartParser, FormParser])
# def verify_csv(request):
#     if request.method == "POST":
#         print("request", request.body)
#         print("request", request.FILES)
#         from .utils.validators import validate_uploaded_csv

#         if request.method == "POST" and request.FILES.get("file"):
#             file = request.FILES["file"]
#             result = validate_uploaded_csv(file, PLAYER_NAMES_PATH, TEAM_NAMES_PATH)
#             errors = result["errors"]
#             logos = result["team_logos"]
#             if errors:
#                 return JsonResponse({"status": "error", "errors": errors}, status=400)
#             return JsonResponse(
#                 {"status": "success", "message": "File is valid.", "team_logos": logos}
#             )
#         return JsonResponse(
#             {
#                 "status": "error",
#                 "message": "No file provided or invalid request method.",
#             },
#             status=400,
#         )


# @csrf_exempt
# def get_players(request):
#     if request.method == "GET":
#         user_input = request.GET.get("user_input")
#         # If user_input is greater than 3 characters, search for player names
#         if len(user_input) > 3:
#             player_names = pd.read_csv(PLAYER_NAMES_PATH)
#             player_names = player_names[
#                 player_names["cricsheet_name"].str.contains(user_input, case=False)
#             ]
#             player_names = player_names["cricsheet_name"].tolist()
#             return JsonResponse({"player_names": player_names})


# @csrf_exempt
# def get_player_data(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         player_name = body['name']
#         date = body['date']
#         model = body['model']
#         stats = get_player_stats(player_name,date,model)
#         return JsonResponse({'stats':stats})
        
# def get_teams():
#     pass

# def get_team_logos_from_team_names():
#     pass

# def get_player_matchups():
#     pass

# def get_player_features():
#     pass
import json
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from players.utils.player_service import get_player_stats, matchup_stats, player_features
# from services.player_service import get_player_stats
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
def get_teams(request):
    if request.method == "GET":
        user_input = request.GET.get('user_input')
        # If user_input is greater than 3 characters, search for team names
        if len(user_input) > 3:
            team_names = pd.read_csv(TEAM_NAMES_PATH)
            team_names = team_names[team_names['name'].str.contains(user_input, case=False)]
            team_names = team_names['name'].tolist()
            return JsonResponse({'team_names': team_names})
        
@csrf_exempt
def get_team_logos_from_team_names(request):
    if request.method == "POST":
        data = json.loads(request.body)
        team_names = data['team_names']
        team_details = pd.read_csv(TEAM_NAMES_PATH)
        team_logos = team_details[team_details['name'].isin(team_names)]
        team_logos = team_logos[['name', 'logo']].to_dict(orient='records')
        return JsonResponse({'team_logos': team_logos})

# @csrf_exempt
# def get_player_data(request):
#     if request.method == "POST":
#         # player_name = request.GET.get('player_name')
#         # date = request.Get.get('date')
#         data = json.loads(request.body)
#         # stats = get_player_stats(player_name,date)
#         return JsonResponse({'stats':"stats", "data": data})

@csrf_exempt
def get_player_data(request):
    if request.method == "POST":
        body = json.loads(request.body)
        player_name = body['name']
        date = body['date']
        model = body['model']
        stats = get_player_stats(player_name,date,model)
        return JsonResponse({'stats':stats})
    

@csrf_exempt
def get_player_matchups(request):
    if request.method == "POST":
        body = json.loads(request.body)
        player_name = body['player_name']
        player_opponents = body['player_opponents'].split(',')
        date = body['date']
        model = body['model']
        stats = matchup_stats(player_name,player_opponents,model,date)
        return JsonResponse({'stats':stats})
    else:
        return JsonResponse({'error':'Only POST request allowed'})
        
@csrf_exempt
def get_player_features(request):
    if request.method == "POST":
        body = json.loads(request.body)
        player_name = body['name']
        date = body['date']
        model = body['model']
        stats = player_features(player_name,date,model)
        return JsonResponse({'stats':stats})
        
@csrf_exempt
def get_22_random_players(request):
    if request.method == "GET":
        players = pd.read_csv("players/utils/matchups.csv")
        players = players["batsman_name"].sample(22)
        players = players['batsman_name'].tolist()
        return JsonResponse({'players':players})
    else:
        return JsonResponse({'error':'Only GET request allowed'})