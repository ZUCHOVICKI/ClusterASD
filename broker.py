from multiprocessing import connection
import socket
from json import loads
import Images
import multiprocessing

class Broker:
    def __init__(self, hostname: str, port: int) -> None:
        self.manager = multiprocessing.Manager()
        self.servidores_procesamiento = []

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

            while True:
                buffer = conn.recv(1024)

                if not buffer:
                    if(isinstance(decoded_json, dict)):
                        self.manejar_mensaje(decoded_json, extra_data)
                        break
                else:
                    if(not decoded_json):
                        # El JSON nunca será mayor a 1024 bytes 
                        decoded_json = loads(buffer)

                        continue_listening = True if decoded_json['message'] == 'CONTINUE' else False

                        if(continue_listening):
                            conn.send(b'1')
                        else:
                            conn.send(b'0')

                        continue
                    if(continue_listening):
                        extra_data += buffer

    def manejar_mensaje(self, mensaje: dict, extra_data: bytes):
        switch_manejador = {
            "NODE_CONNECT": lambda puerto: self.registrar_nodo(puerto),
            "VIDEO": lambda _, video: self.manejar_video(video)
        }

        try:
            switch_manejador[mensaje['type']](mensaje['message'], extra_data)
        except KeyError:
            print("Opción incorrecta en key: Type")

    def registrar_nodo(self, puerto: int):
        if(self.servidores_procesamiento.count(puerto) == 0):
            self.servidores_procesamiento.append(puerto)

            print(f"Servidor procesamiento agregado: {puerto}")
        else:
            print(f"Ya existe un nodo con el puerto: {puerto}")

    def manejar_video(self, video):
        video_file = open('Videos/video.mp4', 'wb')
        video_file.write(video)

        Images.VideoToImage('Videos/video.mp4', 'video_chido')

    def __len__(self):
        return len(self.servidores_procesamiento)


if __name__ == '__main__':
    b = Broker("localhost", 2000)
    b.listen()