from socket import socket

class Broker:
    def __init__(self, hostname: str, port: int) -> None:
        self.servidores_procesamiento = []
        self.socket = socket()

        self.socket.bind((hostname, port))
        self.socket.listen()

        print("Servidor broker iniciado. Esperando nuevas conexiones.")
        
        while True:
            print(f"Número de servidores de procesamiento connectados: {len(self)}")

            conn, address = self.socket.accept()

            print(f"Nueva conexión de {address}")

            self.__manejar_conexion(conn)

    def __manejar_conexion(self, socket: socket) -> None:
        print("Manejando conexión")

        while True:
            buffer = socket.recv(1024)
            data = b""

            if not buffer:
                print(data)
                socket.send(b"END")
                break
            else:
                data += buffer

    def __len__(self):
        return len(self.servidores_procesamiento)

b = Broker("localhost", 2000)