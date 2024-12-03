import json
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from players.utils.player_service import get_player_stats,matchup_stats,player_features
# from services.player_service import get_player_stats
# Create your views here.
PLAYER_NAMES_PATH = 'players/utils/player_names.csv'
TEAM_NAMES_PATH = 'players/utils/team_details.csv'
PLAYER_DATA_PATH = 'players/utils/player_datails.json'

def home(request):        
    return HttpResponse('hello world!')

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