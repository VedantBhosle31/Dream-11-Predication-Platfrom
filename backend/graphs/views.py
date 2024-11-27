from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os

def hello(request):
    return HttpResponse('Hello, World!')

def get_player_points(request):
    if request.method == 'GET':
        player_id = request.GET.get('player_id')
        print(player_id)
        if player_id is None:
            return JsonResponse({'error': 'player_id is required'}, status=400)
        
        csv_file_path = 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/dummy_player_data.csv'

        if not os.path.exists(csv_file_path):
            return JsonResponse({'error': 'CSV file not found'}, status=404)
        
        df = pd.read_csv(csv_file_path)
        
        df_filtered = df[df['Player_ID'] == int(player_id)]
        
        if df_filtered.empty:
            return JsonResponse({'error': 'No data found for the given player_id'}, status=404)
        
        df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])
        df_filtered = df_filtered.sort_values(by='Date', ascending=False).head(10)
        
        data = df_filtered[['Date', 'Previous_Runs']].to_dict(orient='records')
        
        return JsonResponse(data, safe=False)
