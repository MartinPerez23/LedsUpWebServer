from rest_framework import serializers

from .models import Errores


class ErroresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errores
        fields = ['detalle', 'contexto', 'origen']
