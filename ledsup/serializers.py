from rest_framework import serializers

from ledsup.models import Showroom, Dispositivo, User


class ShowroomSerializer(serializers.ModelSerializer):
    dispositivos = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='orden'
    )

    class Meta:
        model = Showroom
        fields = [
            'id',
            'usuario',
            'dispositivos',
            'nombre_showroom',
            'matriz_x_total',
            'matriz_y_total',
            'url_server',
        ]

        extra_kwargs = {'id': {'required': False}}


class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = [
            'id',
            'nombre_dispositivo',
            'numero_ip',
            'universo',
            'tamano_paquetes',
            'matriz_x',
            'matriz_y',
            'patch',
            'fecha_creacion',
            'tipo_led',
        ]

        extra_kwargs = {'id': {'required': False}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
