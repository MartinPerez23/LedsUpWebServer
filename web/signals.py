import cloudinary.uploader
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Evento, ImagenesProducto


@receiver(post_delete, sender=ImagenesProducto)
def borrar_imagen_cloudinary(sender, instance, **kwargs):
    if instance.imagen:
        cloudinary.uploader.destroy(instance.imagen.public_id)


@receiver(post_delete, sender=Evento)
def borrar_imagen_cloudinary(sender, instance, **kwargs):
    if instance.imagen:
        cloudinary.uploader.destroy(instance.imagen.public_id)
