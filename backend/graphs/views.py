from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def hello(request):
    return HttpResponse('Hello, World!')

def get_player_points(request, player_id):
    if request.method == 'GET':
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

def get_player_radar_chart(request, player_id):
    if request.method == 'GET':
        if player_id is None:
            return JsonResponse({'error': 'player_id is required'}, status=400)

        try:
            player_id = int(player_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid player_id'}, status=400)

        csv_files = {
            'batting': 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/data/dummy_player_batter_data.csv',
            'bowling': 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/data/dummy_player_bowler_data.csv',
            'fielding': 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/data/dummy_player_fielding_data.csv',
        }

        for name, path in csv_files.items():
            if not os.path.exists(path):
                return JsonResponse({'error': f'{name} CSV file not found'}, status=404)

        def process_csv(key, path):
            df = pd.read_csv(path)

            df = df[df['player_id'] == player_id]

            if df.empty:
                return {key: {'error': f'No data found for player_id in {key} CSV'}}
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=False)

            df_latest_10 = df.head(10)

            if (key == 'batting'):
                print(df_latest_10)

            columns_map = {
                'batting': ['previous_average', 'previous_strike_rate'],
                'bowling': ['wickets', 'economy'],
                'fielding': ['fielding', 'matchup'],
            }

            result = {}
            for col in columns_map[key]:
                if col not in df_latest_10.columns:
                    return {key: {'error': f'Missing {col} column in {key} CSV'}}

                avg_value = df_latest_10[col].mean()
                print(avg_value)
                max_value = df_latest_10[col].max()
                print(max_value)

                if max_value == 0:
                    normalized_value = 0
                else:
                    normalized_value = (avg_value / max_value) * 100

                result[col] = round(avg_value, 2)

            return {key: result}

        with ThreadPoolExecutor() as executor:
            future_to_csv = {executor.submit(process_csv, key, path): key for key, path in csv_files.items()}
            result = {}

            for future in as_completed(future_to_csv):
                data = future.result()
                result.update(data)

        if 'error' in result.get('batting', {}):
            return JsonResponse(result['batting'], status=404)

        flattened_result = {
            "previous_average": result.get('batting', {}).get('previous_average', 0),
            "previous_strike_rate": result.get('batting', {}).get('previous_strike_rate', 0),
            "wickets": result.get('bowling', {}).get('wickets', 0),
            "economy": result.get('bowling', {}).get('economy', 0),
            "fielding": result.get('fielding', {}).get('fielding', 0),
            "matchup": result.get('fielding', {}).get('matchup', 0)
        }

        return JsonResponse(flattened_result, safe=False)

# def get_player_radar_chart(request):
#     if request.method == 'GET':
#         player_id = request.GET.get('player_id')
#         if player_id is None:
#             return JsonResponse({'error': 'player_id is required'}, status=400)

#         try:
#             player_id = int(player_id)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid player_id'}, status=400)

#         # File paths for the three CSV files
#         csv_files = {
#             'batting': 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/data/dummy_player_batter_data.csv',
#             'bowling': 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/data/dummy_player_bowler_data.csv',
#             'fielding': 'C:/Users/Paurush Kumar/Desktop/Dream-11-Predication-Platfrom/backend/graphs/data/dummy_player_fielding_data.csv',
#         }

#         # Check if all files exist
#         for name, path in csv_files.items():
#             if not os.path.exists(path):
#                 return JsonResponse({'error': f'{name} CSV file not found'}, status=404)

#         # Load all CSVs
#         dfs = {key: pd.read_csv(path) for key, path in csv_files.items()}

#         # Initialize the result dictionary
#         result = {}

#         # Define required columns for each CSV
#         columns_map = {
#             'batting': ['previous_average', 'previous_strike_rate'],
#             'bowling': ['wickets', 'economy'],
#             'fielding': ['fielding', 'matchup'],
#         }

#         for key, df in dfs.items():
#             # Filter by player_id
#             df = df[df['player_id'] == player_id]

#             if df.empty:
#                 return JsonResponse({'error': f'No data found for player_id in {key} CSV'}, status=404)

#             # Convert Date column to datetime and sort by date
#             df['date'] = pd.to_datetime(df['date'])
#             df = df.sort_values(by='date', ascending=False).head(10)

#             # Process required columns
#             for col in columns_map[key]:
#                 if col not in df.columns:
#                     return JsonResponse({'error': f'Missing {col} column in {key} CSV'}, status=400)

#                 avg_value = df[col].mean()  # Calculate average
#                 max_value = df[col].max()  # Get max value

#                 if max_value == 0:  # Avoid division by zero
#                     normalized_value = 0
#                 else:
#                     normalized_value = (avg_value / max_value) * 100

#                 result[col] = round(normalized_value, 2)  # Add normalized value to result

#         return JsonResponse(result, safe=False)