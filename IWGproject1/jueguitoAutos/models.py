from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)  # El RUT será único
    medio_transporte = models.CharField(max_length=50)  # Ejemplo: "Bicicleta", "Automóvil", etc.

    def __str__(self):
        return self.nombre


class RegistroKilometraje(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relaciona cada registro con un usuario
    fecha = models.DateField()  # Fecha del registro
    kilometros_recorridos = models.FloatField()  # Kilómetros recorridos en esa semana

    def __str__(self):
        return f"{self.usuario.nombre} - {self.fecha} - {self.kilometros_recorridos} km"
