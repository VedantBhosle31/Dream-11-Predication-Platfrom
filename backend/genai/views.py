from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World!")

def explain_graph(request):
    if request.method == "POST":
        graph_name = request.POST.get("graph_name")
        player_id = request.POST.get("player_id")
        
        