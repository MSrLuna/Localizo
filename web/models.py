from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Tabla General de Usuarios
class Roles(models.Model):
    nombre = models.CharField(max_length=50)

class Usuario(models.Model):
    rut = models.CharField(max_length=14, default="")
    nombre = models.CharField(max_length=150, default="")
    email = models.CharField(max_length=255, default="")
    telefono = models.IntegerField(default=0)
    direccion = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=128)
    estado = models.CharField(max_length=30, blank=True, null=True)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)

    def set_password(self, raw_password):
        """Establecer la contraseña de forma segura."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verificar la contraseña."""
        return check_password(raw_password, self.password)

# Tablas Admin
class Administrador(Usuario):
    apellido = models.CharField(max_length=150, default="")

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50, default="")
    disponible = models.BooleanField(default=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.DO_NOTHING)
    descripcion = models.TextField()
    fecha_ingreso = models.DateField()
    precio_unitario = models.FloatField()
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # <-- Añadir este campo