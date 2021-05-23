import json
from socket import socket
import os

def main(address: str, port: int):
    s = socket()
    file = None

    try:
        s.connect((address, port))
    except ConnectionRefusedError:
        print(f"No sé pudo conectar al servidor broker en: {address}:{port}. Intentalo de nuevo más tarde.")
        return

    try:
        video_path = input("Ingresa la ruta al video: ")
        file = open(video_path, 'rb')
    except FileNotFoundError:
        print("La ruta ingresada no es válida")
        return

    # El primer paso para el protócolo implementado por el broker es enviar un mensaje JSON que indique que se va a enviar el video
    s.send(b'{"type": "VIDEO", "message":"CONTINUE"}')
    # s.send(b'{"type": "NODE_CONNECT", "message": 9050}')

    # Valor binario que indica si el servidor está listo para recibir los datos binarios del video
    should_continue = s.recv(1024)

    if(should_continue == b'1'):
        # Antes de enviar el video se debe enviar que tan grande es el video. El tamaño del video se envía como un Little Endian 8 bit Integer
        filesize = os.path.getsize('Videos\\Pan-Se-Cae2video.mp4')
        s.send(filesize.to_bytes(8, 'little'))

        for byte in file:
            s.send(byte)

        response = json.loads(s.recv(1024))

        if(response['type'] == "END_ERROR"):
            print(f"El servidor cerró la conexión porque ocurrió un error: f{response['message']}")
    else:
        s.close()
        print("El servidor no aceptó el video. Intentalo de nuevo más tarde.")

        
if __name__ == "__main__":
    main('localhost', 2000)