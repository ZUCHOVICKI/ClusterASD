import socket
import json

class Processing_Server():
    def __init__(self, address: str, port: int, broker_port: int = 2000, max_attempts: int = 3) -> None:
        self.socket_server = socket.socket()
        self.hasBroker = False
        self.address = address
        self.port = port
        self.broker_port = broker_port
        self.max_attempts = max_attempts

        if(self.port == self.broker_port):
            raise ValueError("El puerto asignado al servidor de procesamiento no puede ser el mismo que el del servidor broker")

    def listen(self) -> None:
        self.socket_server.bind((self.address, self.port))
        self.socket_server.listen()

        print(f"Servidor de procesamiento @ {self.address}:{self.port} iniciado")
        
    def searchBroker(self) -> bool:
        print(f"Buscando servidor broker @ localhost:{self.broker_port}")
        print(f"Se realizarán {self.max_attempts} intentos de conexión")

        attempts = 0
        socket_client = socket.socket()

        while (attempts < self.max_attempts):
            try:
                socket_client.connect(('localhost', self.broker_port))
                request_json = {"type": "NODE_CONNECT", "message": self.port}

                socket_client.send(json.dumps(request_json).encode('ASCII'))

                response = socket_client.recv(1024)
                
                try:
                    response = json.loads(response)

                    if(response['type'] == 'NODE_CONNECTED'):
                        socket_client.close()
                        return True
                    if(response['type'] == 'NODE_EXISTS'):
                        print(f"Ya existe un servidor de procesamiento con el puerto: {self.port}")
                        raise ValueError
                except:
                    continue
            except:
                print("Fallo al conectarse con el servidor broker")
                attempts += 1

        socket_client.close()
        return False

    def kill(self) -> None:
        self.socket_server.close()

if __name__ == '__main__':
    s = Processing_Server('localhost', 9560)
    
    if(s.searchBroker()):
        print("Conectado al servidor broker")
        s.kill()
    else:
        print("Fallaron los intentos de conexión al broker")
        s.kill()
