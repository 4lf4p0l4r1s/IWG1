from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página de inicio
    path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
    path('registrar_kilometraje/', views.registrar_kilometraje, name='registrar_kilometraje'),
]
