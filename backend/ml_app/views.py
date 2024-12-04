from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ml_app.utils.ml_service import predict
from players.utils.player_service import fetch_all_player_features
from django.http import JsonResponse
import json

@csrf_exempt
def get_predictions(request):
    if request.method == "POST":
        body = json.loads(request.body)
        names = body['names']
        date = body['date']
        model = body['model']
        pred = predict(names,date,model)
        return JsonResponse(pred)
    
@csrf_exempt
def get_all_player_features(request):
    if request.method == "POST":
        body = json.loads(request.body)
        names = body['names'].split(',')
        date = body['date']
        model = body['model']
        features = fetch_all_player_features(names, date, model)
        return JsonResponse(features)
    else:
        return JsonResponse({'error':'Only POST request allowed'})