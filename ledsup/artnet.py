from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def enviarAlServer(user, datosAEnviar):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "user_" + str(user),
        {
            "type": "enviarAlServer",
            "data": datosAEnviar
        }
    )


def probar_dispositivo(user, listaDispositivos):
    datosAEnviar = {
        'lista': listaDispositivos,
        'accion': 'probar'
    }
    enviarAlServer(user, datosAEnviar)


def color(user, listaDispositivos, colorHex, velocidad, cambio_constante):
    datosAEnviar = {
        'accion': 'color',
        'color': colorHex,
        'velocidad': velocidad,
        'cambio_constante': cambio_constante,
        'lista': listaDispositivos
    }
    enviarAlServer(user, datosAEnviar)


def scroll(user, listaDispositivos, direccion, velocidad):
    datosAEnviar = {
        'accion': 'scroll',
        'direccion': direccion,
        'velocidad': velocidad,
        'lista': listaDispositivos
    }

    enviarAlServer(user, datosAEnviar)


def scan(user, listaDispositivos, direccion, velocidad, colorScan, colorFondo):
    datosAEnviar = {
        'accion': 'scan',
        'direccion': direccion,
        'velocidad': velocidad,
        'colorScan': colorScan,
        'colorFondo': colorFondo,
        'lista': listaDispositivos
    }

    enviarAlServer(user, datosAEnviar)


def estrellas(user, listaDispositivos, velocidad, colorEstrellas, colorFondo):
    datosAEnviar = {
        'accion': 'estrellas',
        'colorEstrellas': colorEstrellas,
        'colorFondo': colorFondo,
        'velocidad': velocidad,
        'lista': listaDispositivos
    }

    enviarAlServer(user, datosAEnviar)
