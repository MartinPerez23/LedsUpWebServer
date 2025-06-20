import datetime
import secrets

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils import timezone


class Dispositivo(models.Model):
    TIPO_LED = [
        ('RGB', 'RGB'),
        ('RBG', 'RBG'),
        ('BRG', 'BRG'),
        ('BGR', 'BGR'),
        ('GRB', 'GRB'),
        ('GBR', 'GBR')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    nombre_dispositivo = models.CharField(max_length=100)
    numero_ip = models.CharField(max_length=15)
    universo = models.PositiveSmallIntegerField(default=0)
    tamano_paquetes = models.PositiveSmallIntegerField(default=512)
    matriz_x = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(5), MaxValueValidator(34)])
    matriz_y = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(5), MaxValueValidator(34)])
    fecha_creacion = models.DateTimeField('Fecha de creacion', default=timezone.now)
    patch = models.TextField(max_length=600, default='Sin patch')
    tipo_led = models.CharField(choices=TIPO_LED, max_length=5, default='RGB')

    @admin.display(
        boolean=True,
        ordering='fecha_creacion',
        description='Creado Recientemente?'
    )
    def creado_recientemente(self):
        hoy = timezone.now()
        return hoy - datetime.timedelta(days=1) <= self.fecha_creacion <= hoy

    def __str__(self):
        return self.nombre_dispositivo


class Showroom(models.Model):
    dispositivos = models.ManyToManyField(
        Dispositivo,
        through='OrdenDispositivosEnShowroom'
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    nombre_showroom = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_showroom + ' creado por: ' + self.usuario.email


class OrdenDispositivosEnShowroom(models.Model):
    ORDEN_DISPOSITIVOS = [
        ('Abajo-Izquierda', 'Abajo-Izquierda'),
        ('Abajo', 'Abajo'),
        ('Abajo-Derecha', 'Abajo-Derecha'),
        ('Izquierda', 'Izquierda'),
        ('Centro', 'Centro'),
        ('Derecha', 'Derecha'),
        ('Arriba-Izquierda', 'Arriba-Izquierda'),
        ('Arriba', 'Arriba'),
        ('Arriba-Derecha', 'Arriba-Derecha')
    ]

    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)

    orden = models.CharField(choices=ORDEN_DISPOSITIVOS, max_length=20, default='Centro')

    def __str__(self):
        return self.orden

class UserConnectionStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    connected = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username}: {'Conectado' if self.connected else 'Desconectado'}"