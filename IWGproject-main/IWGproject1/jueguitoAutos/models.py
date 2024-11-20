from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Definimos el Manager para nuestro modelo de usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, nombre, rut, password=None):
        if not nombre:
            raise ValueError("El nombre debe ser proporcionado")
        user = self.model(nombre=nombre, rut=rut)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre, rut, password=None):
        user = self.create_user(nombre, rut, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Definimos el modelo de Usuario que hereda de AbstractBaseUser
class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)  # El RUT será único
    medio_transporte = models.CharField(max_length=50, choices=[('auto', 'Auto'), ('bus', 'Bus'), ('bicicleta', 'Bicicleta'), ('a pie', 'A pie')])
    huella_carbono_total = models.FloatField(default=0.0)
    # Campos de autenticación
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Especifica el campo para el login
    USERNAME_FIELD = 'rut'  # o 'nombre' si prefieres usar el nombre como nombre de usuario
    REQUIRED_FIELDS = ['nombre']  # Campos que serán requeridos además de USERNAME_FIELD

    objects = UsuarioManager()

    def __str__(self):
        return self.rut

    @property
    def is_staff(self):
        return self.is_admin

# Modelo de RegistroKilometraje que está relacionado con Usuario
class RegistroKilometraje(models.Model):
    MEDIOS_TRANSPORTE = [
        ('auto', 'Auto'),
        ('bus', 'Bus'),
        ('bicicleta', 'Bicicleta'),
        ('a pie', 'A pie'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relaciona cada registro con un usuario
    fecha = models.DateField()  # Fecha del registro
    kilometros_recorridos = models.FloatField()  # Kilómetros recorridos en esa semana
    medio_transporte = models.CharField(max_length=20, choices=MEDIOS_TRANSPORTE)  # Medio de transporte utilizado

    def __str__(self):
        return f"{self.usuario.nombre} - {self.fecha} - {self.kilometros_recorridos} km - {self.medio_transporte}"

    def calcular_emisiones(self):
        """
        Calcula las emisiones generadas por este registro de kilometraje.
        """
        EMISIONES_TRANSPORTE = {
            'auto': 0.21,       # Emisiones en kg CO2/km para un auto
            'bus': 0.1,         # Emisiones en kg CO2/km para un bus
            'bicicleta': 0.0,   # Bicicleta no genera emisiones
            'a pie': 0.0,       # Caminar no genera emisiones
        }
        factor_emision = EMISIONES_TRANSPORTE.get(self.medio_transporte, 0.0)
        return self.kilometros_recorridos * factor_emision

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para actualizar la huella de carbono acumulada del usuario
        al guardar un registro nuevo o actualizado.
        """
        # Calcula las emisiones de este registro
        emisiones = self.calcular_emisiones()

        # Actualiza la huella de carbono acumulada del usuario
        self.usuario.huella_carbono_total += emisiones
        self.usuario.save()

        # Guarda el registro
        super().save(*args, **kwargs)
