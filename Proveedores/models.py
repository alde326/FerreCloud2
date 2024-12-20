from django.db import models
from Inventario.models import Producto

class Proveedor(models.Model):
    nit = models.CharField(max_length=100)
    razonSolcial = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.CharField(max_length=255, null=True, blank=True) 
    nombreContacto = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    eliminado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.razonSolcial


class Reabastecimiento(models.Model):
    estado = models.IntegerField(null=True, blank=True, default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    fechaEsperada = models.DateTimeField(null=True, blank=True)
    fechaLlegada = models.DateTimeField(null=True, blank=True)
    credito = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=200)

class ReabastecimientoDetalle(models.Model):
    reabastecimiento_id = models.ForeignKey(Reabastecimiento, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    credito = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'