from json import loads, dumps, dump
from names.words import GetName
from typing import Optional

import socket
import Images
import os
import math

class Broker:
    def __init__(self, hostname: str, port: int) -> None:
        self.servidores_procesamiento = [1000, 2000, 3000]

        self.socket = socket.socket()
        self.hostname = hostname
        self.port = port

    def listen(self) -> None:
        self.socket.bind((self.hostname, self.port))
        self.socket.listen()

        print("Servidor broker iniciado. Esperando nuevas conexiones.")

        while True:
            print(f"Número de servidores de procesamiento registrados: {len(self)}")

            conn, address = self.socket.accept()

            print(f"Nueva conexión de {address}")
            print("Manejando conexión")

            continue_listening = False
            decoded_json = b""
            extra_data = b""
            extra_data_size = 0

            while True:
                buffer = conn.recv(1024)
                recieved_bytes = len(buffer)

                if not buffer:
                    break
                else:
                    if(not decoded_json):
                        # El JSON nunca será mayor a 1024 bytes 
                        decoded_json = loads(buffer)

                        continue_listening = True if decoded_json['message'] == 'CONTINUE' else False

                        if(continue_listening):
                            conn.send(b'1')
                        else:
                            break

                        continue
                    if(continue_listening):
                        if(not extra_data_size):
                            extra_data_size = int.from_bytes(buffer, 'little')
                            conn.send(b'1')
                        else:
                            if(extra_data_size >= 0):
                                extra_data += buffer
                                extra_data_size -= recieved_bytes
                            # El protocolo debe avisar cuando haya terminado de leer el archivo enviado
                            # para que el cliente empieze a esperar la respuesta
                            if(extra_data_size <= 0):
                                conn.send(b'1')
                                break

            if(isinstance(decoded_json, dict)):
                self.manejar_mensaje(decoded_json, extra_data, conn)
                conn.close()

    def manejar_mensaje(self, mensaje: dict, extra_data: bytes, socket: Optional[socket.socket] = None):
        switch_manejador = {
            "NODE_CONNECT": lambda puerto, _, socket: self.registrar_nodo(puerto, socket),
            "VIDEO": lambda _, video, socket: self.manejar_video(video, socket)
        }

        try:
            switch_manejador[mensaje['type']](mensaje['message'], extra_data, socket)
        except KeyError:
            print("Opción incorrecta en key: Type")
            socket.send(b'{"type": "END_ERROR", "message":"Opcion incorrecta en key: Type del JSON de la peticion"}')

    def registrar_nodo(self, puerto: int, socket: socket.socket):
        response_json = {}

        if(self.servidores_procesamiento.count(puerto) == 0):
            self.servidores_procesamiento.append(puerto)
            response_json = {"type": "NODE_CONNECTED", "message": puerto}

            print(f"Servidor procesamiento agregado: {puerto}")
        else:
            response_json = {"type": "NODE_EXISTS", "message": puerto}
            print(f"Ya existe un nodo con el puerto: {puerto}")

        socket.send(dumps(response_json).encode('ASCII'))

    def manejar_video(self, video, socket):
        if(len(self) == 0):
            print("No hay ningun servidor de procesamiento registrado")
            return

        video_name = GetName()

        video_file = open(f'Videos/{video_name}.mp4', 'wb')
        video_file.write(video)

        Images.VideoToImage(f'Videos/{video_name}.mp4', video_name)

        frames = []

        for item in os.listdir(f'Images{video_name}/'):
            if(os.path.isfile(f"Images{video_name}/{item}")):
                frames.append(item)

        images_to_share = math.floor(len(frames) / len(self)) + 1
        shared_images = 0

        for i in range(len(self)):
            if(i != len(self) - 1):
                print(f"Enviando al servidor {i} para que procese imagenes del {shared_images + 1} a {shared_images + images_to_share}")
                shared_images += images_to_share
            else:
                print(f"Enviando al servidor {i} para que procese imagenes del {shared_images + 1} a {len(frames) - 1}")

        socket.send(b'{"type": "VIDEO_COMPLETE"}')
                
    def __len__(self):
        return len(self.servidores_procesamiento)


if __name__ == '__main__':
    b = Broker("localhost", 2000)
    b.listen()