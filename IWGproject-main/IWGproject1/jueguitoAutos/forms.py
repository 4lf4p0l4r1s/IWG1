from django import forms
from .models import RegistroKilometraje, Usuario  # Solo importamos lo necesario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Para usar el formulario de creación de usuario de Django

# Formulario para el Usuario
class UsuarioForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, label='Nombre Completo')
    rut = forms.CharField(max_length=12, label='ROL (sin puntos con guión)',
                          widget=forms.TextInput(attrs={'placeholder': 'Ej. 202471412-3'})
                          )

    class Meta:
        model = Usuario  # Asegúrate de que Usuario es el modelo correcto
        fields = ['nombre', 'rut', 'password1', 'password2']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        # Puedes agregar validación aquí, como comprobar el formato del RUT
        return rut

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="ROL USM", max_length=12)  # ROL del usuario
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)  # Contraseña

# Formulario para Registro de Kilometraje
from django.forms import DateInput
class RegistroKilometrajeForm(forms.ModelForm):
    # Definir el campo 'usuario' fuera del bloque Meta
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione un usuario",  # Esto asegura que se muestre una opción por defecto
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = RegistroKilometraje
        fields = ['usuario', 'fecha', 'kilometros_recorridos', 'medio_transporte']

        widgets = {
            'fecha': DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Widget para el campo de fecha
            'kilometros_recorridos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los kilómetros recorridos'
            }),
            'medio_transporte': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'usuario': 'Usuario (ROL)',  # Puedes cambiar el nombre del campo según lo que necesites
            'fecha': 'Fecha',
            'kilometros_recorridos': 'Kilómetros recorridos',
            'medio_transporte': 'Medio de transporte utilizado',
        }
