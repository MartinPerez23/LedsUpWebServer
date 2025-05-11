import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


def ruta_imagen_producto(instance, filename):
    extension = filename.split('.')[-1]
    nombre_imagen_con_extension = instance.nombre_imagen + '.' + extension
    ruta = 'web/static/web/imagenes/productos/producto_{0}/{1}'.format(instance.producto.id,
                                                                       nombre_imagen_con_extension)

    return ruta


def ruta_imagen_galeria(instance, filename):
    extension = filename.split('.')[-1]
    nombre_imagen_con_extension = instance.nombre_imagen + '.' + extension
    ruta = 'web/static/web/imagenes/galeria/evento_{0}/{1}'.format(instance.galeria.id,
                                                                   nombre_imagen_con_extension)

    return ruta


class TipoProducto(models.Model):
    nombre_tipo_producto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo_producto


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    detalles = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField('Fecha de creacion', default=timezone.now)

    @admin.display(
        boolean=True,
        ordering='fecha_creacion',
        description='Creado Recientemente?'
    )
    def creado_recientemente(self):
        hoy = timezone.now()
        return hoy - datetime.timedelta(days=1) <= self.fecha_creacion <= hoy

    def __str__(self):
        return self.nombre_producto


class CaracteristicasProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    texto_caracteristica = models.CharField(max_length=50)

    def __str__(self):
        return self.texto_caracteristica


class ImagenesProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_imagen = models.CharField(max_length=100)

    imagen = models.ImageField('img', upload_to=ruta_imagen_producto, null=True, blank=True)

    @property
    def url(self):
        url_modificada = self.imagen.url.replace('web/static', '')
        return url_modificada

    def __str__(self):
        return self.nombre_imagen


class VideosProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_video = models.CharField(max_length=100)
    url_video = models.URLField(max_length=200, null=True)

    def __str__(self):
        return self.nombre_video


class Galeria(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField('Fecha de creacion', default=timezone.now)
    detalle = models.TextField()

    def __str__(self):
        return self.nombre

class ImagenesGaleria(models.Model):
    galeria = models.ForeignKey(Galeria, on_delete=models.CASCADE)
    nombre_imagen = models.CharField(max_length=100)

    imagen = models.ImageField('img', upload_to=ruta_imagen_galeria, null=True, blank=True)

    @property
    def url(self):
        url_modificada = self.imagen.url.replace('web/static', '')
        return url_modificada

    def __str__(self):
        return self.nombre_imagen
