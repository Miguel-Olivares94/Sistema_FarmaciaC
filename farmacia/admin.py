
from django.contrib import admin
from .models import Medicamento, Proveedor, Venta, DetalleVenta  # Reemplaza con los nombres reales de tus modelos en "collico_sw"

admin.site.register(Medicamento)
admin.site.register(Proveedor)
admin.site.register(Venta)
admin.site.register(DetalleVenta)