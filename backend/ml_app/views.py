from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pickle
import json
import pandas as pd

# Create your views here.
MODEL_PATH = 'ml_app/model.pkl'


with open(MODEL_PATH,'rb') as file:
    model = pickle.load(file)

def home(request):
    return HttpResponse('hello world!')

from django.http import JsonResponse
import json

@csrf_exempt
def predict(request):
    if request.method == "POST":
        try:
            # Parse the body
            body = json.loads(request.body)

            # Get `names` and `date` from the parsed body
            names = body.get("names")
            date = body.get("date")
            print(names)
            print(date)
            # Validate inputs
            if not names or not date:
                return JsonResponse({"error": "Missing 'names' or 'date' in request body"}, status=400)
            names = names.split(',')
            for i in range(len(names)):
                names[i]=names[i].strip(" ")
            # Assuming `model.predict()` returns a pandas DataFrame or an array
            try :
                result = model.predict(names, date)
            except Exception as e:
                return JsonResponse({"error": f"{str(e)}"}, status=500)

            # Process result based on its type
            if isinstance(result, pd.DataFrame):
                data_dict = result.to_dict(orient='list')
            else:
                data_dict = {'predictions': result.tolist()}

            # Return the JSON response
            return JsonResponse(data_dict, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    else:
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)
