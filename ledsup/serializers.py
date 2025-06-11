from rest_framework import serializers

from ledsup.models import Showroom, Dispositivo, User, OrdenDispositivosEnShowroom


class ShowroomSerializer(serializers.ModelSerializer):
    dispositivos = serializers.SerializerMethodField()

    class Meta:
        model = Showroom
        fields = ['id', 'usuario', 'dispositivos', 'nombre_showroom']

    def get_dispositivos(self, obj):
        ordenes = OrdenDispositivosEnShowroom.objects.filter(showroom=obj)
        return OrdenDispositivoSerializer(ordenes, many=True).data


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

class OrdenDispositivoSerializer(serializers.ModelSerializer):
    nombre_dispositivo = serializers.CharField(source='dispositivo.nombre_dispositivo')
    id_dispositivo = serializers.IntegerField(source='dispositivo.id')

    class Meta:
        model = OrdenDispositivosEnShowroom
        fields = ['id_dispositivo', 'nombre_dispositivo', 'orden']