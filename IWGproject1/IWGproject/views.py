from django.shortcuts import render

def home(request):
    # lógica para la vista home
    return render(request, 'home.html')

