# farmacia/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.models import User


class Medicamento(models.Model):
    sku = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    laboratorio = models.CharField(max_length=255)
    principio_activo = models.CharField(max_length=255)
    accion_terapeutica = models.CharField(max_length=255)
    presentacion = models.CharField(max_length=255)
    dosis = models.CharField(max_length=255)
    bioequivalente = models.CharField(max_length=255)
    stock = models.PositiveIntegerField(default=0)
    precio = models.PositiveIntegerField()
    proveedor = models.CharField(max_length=255)
    nivel_stock = models.CharField(max_length=255, blank=True, null=True)
    fecha_ingreso = models.DateField()
    fecha_vencimiento = models.DateField()
  
    def calcular_precio_total_vendido(self):
        return sum(detalle.precio_total() for detalle in self.detalleventa_set.all())

 

    def get_nivel_stock(self):
        if self.stock < 100:
            return 'Bajo'
        elif 100 <= self.stock < 700:
            return 'Medio'
        else:
            return 'Alto'

    def __str__(self):
        return self.nombre




class Venta(models.Model):
    medicamento = models.ForeignKey('Medicamento', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_realizadas')

 

class DetalleVenta(models.Model):
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    medicamento = models.ForeignKey('Medicamento', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    

    def precio_total(self):
        return self.cantidad * self.precio_unitario


    def __str__(self):
        return f'Detalle de Venta {self.id}'


# Proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    razon_social = models.CharField(max_length=255)
    rut = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    email = models.EmailField()
    fono = models.CharField(max_length=20)
    productos = models.TextField()

    def get_absolute_url(self):
        return reverse('proveedor_detail', args=[str(self.id)])

    def __str__(self):
        return self.nombre
