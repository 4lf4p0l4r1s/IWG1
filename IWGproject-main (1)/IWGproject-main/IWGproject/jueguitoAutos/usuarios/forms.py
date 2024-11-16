from django import forms
from .models import RegistroKilometraje, Usuario

class RegistroKilometrajeForm(forms.ModelForm):
    class Meta:
        model = RegistroKilometraje
        fields = ['usuario', 'fecha', 'kilometros_recorridos']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'rut', 'medio_transporte']
