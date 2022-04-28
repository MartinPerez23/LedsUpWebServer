import json
import socket

HOST, PORT = "localhost", 8000


def enviarAlServer(datosAEnviar):
    jsonParaEnviar = json.dumps(datosAEnviar)
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(jsonParaEnviar + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

    print("Sent:     {}".format(jsonParaEnviar))
    print("Received: {}".format(received))


def probar_dispositivo(listaDispositivos):
    datosAEnviar = {
        'lista': listaDispositivos,
        'accion': 'probar'
    }
    enviarAlServer(datosAEnviar)


def color(listaDispositivos, colorHex):

    datosAEnviar = {
        'accion': 'color',
        'color': colorHex,
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
