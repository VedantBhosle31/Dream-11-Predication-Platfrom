from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pickle
import json
import pandas as pd
from ml_app.utils.ml_service import predict

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