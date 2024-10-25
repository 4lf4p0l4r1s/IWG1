from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse

def obtener_datos_api(request):
    url = "https://api.example.com/endpoint"  # Cambia esto por la URL de tu API
    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()  
        return JsonResponse(datos, safe=False)  
    else:
        return JsonResponse({"error": "No se pudo obtener los datos"}, status=response.status_code)
