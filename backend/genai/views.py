from django.http import JsonResponse, HttpResponse
import json
from genai.utils.explain_graph import graph_explain
from genai.utils.player_info import player_description

def home(request):
    return HttpResponse("Hello, World!")

def explain_graph(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            graph_name = body.get('graph_name')
            if not graph_name:
                return JsonResponse({'error': 'graph_name is required'}, status=400)
            
            data = json.dumps(body)
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
            if not feature_name:
                return JsonResponse({'error': 'feature_name is required'}, status=400)
            data = json.dumps(body)
            description = player_description(data,feature_name, user_task)
            return JsonResponse({'description': description}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)