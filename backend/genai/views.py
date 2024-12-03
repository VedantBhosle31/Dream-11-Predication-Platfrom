from django.http import JsonResponse, HttpResponse
import json
from genai.utils.explain_graph import graph_explain
from genai.utils.player_info import player_description
from genai.utils.get_data import get_data

def home(request):
    return HttpResponse("Hello, World!")

def explain_graph(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            graph_name = body.get('graph_name')
            player_name = body.get('player_name')
            date = body.get('date')
            model = body.get('model')
            player_opponents = body.get('player_opponents').split(',') if body.get('player_opponents') else []
            player_type = body.get('player_type')
            opponent = body.get('opponent')

            if not graph_name or not player_name or not date or not model:
                return JsonResponse({'error': 'graph_name, player_name, date and model are required'}, status=400)
            if not player_opponents:
                return JsonResponse({'error': 'player_opponents is required'}, status=400)
            if not player_type:
                player_type = 'batter'
            data = json.dumps(get_data(player_type, graph_name, player_name, date, model, player_opponents))
            explanation = graph_explain(graph_name, data)
            return JsonResponse({'explanation': explanation}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid JSON'})


def describe_player(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            feature_name = body['feature_name']
            user_task = body.get('user_task', '')
            player_name = body.get('player_name')
            date = body.get('date')
            model = body.get('model')
            player_opponents = body.get('player_opponents').split(',') if body.get('player_opponents') else []
            player_type = body.get('player_type')

            if not feature_name:
                return JsonResponse({'error': 'feature_name is required'}, status=400)
            if not player_name or not date or not model:
                return JsonResponse({'error': 'player_name, date and model are required'}, status=400)
            data = json.dumps(get_data(player_type, feature_name, player_name, date, model, player_opponents))
            description = player_description(data,feature_name, user_task)
            return JsonResponse({'description': description}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)