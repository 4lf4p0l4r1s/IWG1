from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from .models import RegistroKilometraje, Usuario
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Usuario, RegistroKilometraje
from .forms import RegistroKilometrajeForm, UsuarioForm




from django.db.models import Sum, F, Case, When, Value, FloatField
def ranking(request):
    # Calcular la huella de carbono total acumulada para cada usuario
    usuarios = Usuario.objects.annotate(
        huella_carbono_acumulada=Sum(
            Case(
                # Calcular la huella de carbono en función de los kilómetros recorridos y el medio de transporte
                When(registrokilometraje__medio_transporte='auto', then=F('registrokilometraje__kilometros_recorridos') * 0.21),
                When(registrokilometraje__medio_transporte='bus', then=F('registrokilometraje__kilometros_recorridos') * 0.04),
                When(registrokilometraje__medio_transporte='bicicleta', then=Value(0)),  # No huella para bicicleta
                When(registrokilometraje__medio_transporte='a_pie', then=Value(0)),  # No huella para ir a pie
                default=Value(0),  # Valor por defecto en caso de no coincidir con ninguna opción
                output_field=FloatField()
            )
        )
    ).order_by('huella_carbono_total')[:10]  # Limitar a los 10 usuarios con menor huella de carbono

    return render(request, 'ranking.html', {'usuarios': usuarios})

from django.contrib import messages


def login_usuario(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        password = request.POST.get('password')

        # Autenticación del usuario con el RUT como nombre de usuario
        user = authenticate(request, username=rut, password=password)

        if user is not None:
            # Si las credenciales son correctas, loguear al usuario
            login(request, user)
            return redirect('dashboard')
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            messages.error(request, "Credenciales inválidas. Intenta nuevamente.")
            return redirect('login_usuario')  # Redirigir al formulario de login nuevamente

    return render(request, 'login.html')  # Mostrar el formulario de login si la solicitud es GET


def registro_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_kilometraje')  # Cambia 'registrar_kilometraje' por el nombre correcto de la URL
    else:
        form = UsuarioForm()
    return render(request, 'registro_usuario.html', {'form': form})

def calcular_huella_carbono(kilometros, medio_transporte):
    factores_emision = {
        'auto': 0.21,      # kg CO₂/km
        'bus': 0.09,       # kg CO₂/km
        'bicicleta': 0.0,  # Sin emisiones
        'a pie': 0.0,      # Sin emisiones
    }
    return kilometros * factores_emision.get(medio_transporte, 0)


def registrar_kilometraje(request):
    if request.method == "POST":
        form = RegistroKilometrajeForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            kilometros = form.cleaned_data['kilometros_recorridos']
            medio_transporte = form.cleaned_data['medio_transporte']  # Medio de transporte seleccionado

            # Calcular la huella de carbono
            huella_carbono = calcular_huella_carbono(kilometros, medio_transporte)

            # Guardar el registro de kilometraje
            registro = form.save(commit=False)
            registro.usuario = usuario
            registro.save()

            # Después de guardar el registro, actualizamos la huella de carbono acumulada del usuario
            usuario.huella_carbono_total = sum(
                r.calcular_emisiones() for r in RegistroKilometraje.objects.filter(usuario=usuario)
            )
            usuario.save()

            return redirect('registrar_kilometraje')
    else:
        form = RegistroKilometrajeForm()

    return render(request, 'registrar_kilometraje.html', {'form': form})


def index(request):
    return render(request, 'paginita.html')

def obtener_datos_api(request):
    url = "https://api.example.com/endpoint"  # Cambia esto por la UR1L de tu API
    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()  
        return JsonResponse(datos, safe=False)  
    else:
        return JsonResponse({"error": "No se pudo obtener los datos"}, status=response.status_code)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Usuario, RegistroKilometraje

@login_required
def dashboard(request):
    usuario = request.user  # Usuario autenticado
    # Obtener todos los registros de kilometraje del usuario
    registros = RegistroKilometraje.objects.filter(usuario=usuario)

    # Calcular el total de kilómetros recorridos
    total_kilometros = registros.aggregate(total=Sum('kilometros_recorridos'))['total'] or 0

    # Obtener el medio de transporte más utilizado
    medio_transporte_mas_utilizado = registros.values('medio_transporte').annotate(
        count=Count('medio_transporte')
    ).order_by('-count').first()

    # Mostrar datos del usuario y su información de kilometraje
    context = {
        'usuario': usuario,
        'registros': registros,
        'total_kilometros': total_kilometros,
        'medio_transporte_mas_utilizado': medio_transporte_mas_utilizado
    }

    return render(request, 'dashboard.html', context)
