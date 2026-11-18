from django.db import models

# Create your models here.
class clientes(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10)

class productos(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Para guardar precios con decimales