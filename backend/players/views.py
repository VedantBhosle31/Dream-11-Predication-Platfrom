from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse
# from services.player_service import get_player_stats
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
PLAYER_NAMES_PATH = 'players/utils/player_names.csv'
TEAM_NAMES_PATH = 'players/utils/team_details.csv'
PLAYER_DATA_PATH = 'players/utils/player_datails.json'

def home(request):        
    return HttpResponse('hello world!')

@csrf_exempt
def verify_csv(request):
    if request.method == "POST" and request.FILES.get("file"):
        from .utils.validators import validate_uploaded_csv
        # return JsonResponse({"status": "success", "message": "File is valid."})

        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            errors = validate_uploaded_csv(file, PLAYER_NAMES_PATH, TEAM_NAMES_PATH)
            if errors:
                return JsonResponse({"status": "error", "errors": errors}, status=400)
            return JsonResponse({"status": "success", "message": "File is valid."})
        return JsonResponse({"status": "error", "message": "No file provided or invalid request method."}, status=400)
    
@csrf_exempt
def get_players(request):
    if request.method == "GET":
        user_input = request.GET.get('user_input')
        # If user_input is greater than 3 characters, search for player names
        if len(user_input) > 3:
            player_names = pd.read_csv(PLAYER_NAMES_PATH)
            player_names = player_names[player_names['cricsheet_unique_name'].str.contains(user_input, case=False)]
            player_names = player_names['cricsheet_unique_name'].tolist()
            return JsonResponse({'player_names': player_names})
        
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
def get_player_data(request):
    if request.method == "POST":
        # player_name = request.GET.get('player_name')
        # date = request.Get.get('date')
        data = json.loads(request.body)
        # stats = get_player_stats(player_name,date)
        return JsonResponse({'stats':"stats", "data": data})
        
        