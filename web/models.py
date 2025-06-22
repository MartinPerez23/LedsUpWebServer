import datetime

from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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
    imagen = CloudinaryField('image', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.imagen and hasattr(self.imagen, 'file'):
            upload_result = upload(
                self.imagen.file,
                folder='productos'
            )
            self.imagen = upload_result["public_id"]
        super().save(*args, **kwargs)

    @property
    def url(self):
        from cloudinary.utils import cloudinary_url
        if self.imagen and isinstance(self.imagen, str):
            url, _ = cloudinary_url(self.imagen)
            return url
        return ''

    def __str__(self):
        return self.nombre_imagen


class VideosProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre_video = models.CharField(max_length=100)
    url_video = models.URLField(max_length=200, null=True)

    def __str__(self):
        return self.nombre_video


class Evento(models.Model):
    nombre_evento = models.CharField(max_length=100)
    fecha_de_evento = models.DateTimeField('Fecha de Evento', default=timezone.now)
    pie_de_imagen = models.TextField()

    imagen = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.nombre_evento

    def save(self, *args, **kwargs):
        if self.imagen and hasattr(self.imagen, 'file'):
            upload_result = upload(
                self.imagen.file,
                folder='eventos'
            )
            self.imagen = upload_result["public_id"]

        super().save(*args, **kwargs)


class Errores(models.Model):
    class Meta:
        verbose_name = "Error"
        verbose_name_plural = "Errores"

    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    detalle = models.TextField()
    contexto = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignado_a = models.ForeignKey(User, related_name='errores_asignados', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    comentarios = models.TextField(blank=True, null=True)

    origen = models.CharField(max_length=50, choices=[
        ('web', 'Web'),
        ('app', 'Aplicación de escritorio'),
        ('api', 'API REST'),
        ('otro', 'Otro')
    ])
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('resuelto', 'Resuelto')
    ], default='pendiente')

    def __str__(self):
        return f"Error #{self.id} - {self.origen} - {self.estado}"
