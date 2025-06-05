from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def enviarAlServer(datosAEnviar):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "pc_apps",
        {
            "type": "enviarAlServer",
            "data": datosAEnviar
        }
    )


def probar_dispositivo(listaDispositivos):
    datosAEnviar = {
        'lista': listaDispositivos,
        'accion': 'probar'
    }
    enviarAlServer(datosAEnviar)


def color(listaDispositivos, colorHex, velocidad, cambio_constante):
    datosAEnviar = {
        'accion': 'color',
        'color': colorHex,
        'velocidad': velocidad,
        'cambio_constante': cambio_constante,
        'lista': listaDispositivos
    }
    enviarAlServer(datosAEnviar)


def scroll(listaDispositivos, direccion, velocidad):
    datosAEnviar = {
        'accion': 'scroll',
        'direccion': direccion,
        'velocidad': velocidad,
        'lista': listaDispositivos
    }

    enviarAlServer(datosAEnviar)


def scan(listaDispositivos, direccion, velocidad, colorScan, colorFondo):
    datosAEnviar = {
        'accion': 'scan',
        'direccion': direccion,
        'velocidad': velocidad,
        'colorScan': colorScan,
        'colorFondo': colorFondo,
        'lista': listaDispositivos
    }

    enviarAlServer(datosAEnviar)


def estrellas(listaDispositivos, velocidad, colorEstrellas, colorFondo):
    datosAEnviar = {
        'accion': 'estrellas',
        'colorEstrellas': colorEstrellas,
        'colorFondo': colorFondo,
        'velocidad': velocidad,
        'lista': listaDispositivos
    }

    enviarAlServer(datosAEnviar)
