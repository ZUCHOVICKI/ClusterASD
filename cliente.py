from socket import socket
import os

def main(address: str, port: int):
    s = socket()
    f = None

    try:
        s.connect((address, port))
    except ConnectionRefusedError:
        print(f"No sé pudo conectar al servidor broker en: {address}:{port}. Intentalo de nuevo más tarde.")
        return

    try:
        video_path = input("Ingresa la ruta al video: ")
        f = open(video_path, 'rb')
    except FileNotFoundError:
        print("La ruta ingresada no es válida")
        return

    b_array = []

    s.send(b'{"type": "VIDEO", "message":"CONTINUE"}')
    # s.send(b'{"type": "NODE_CONNECT", "message": 9050}')

    should_continue = s.recv(1024)

    if(should_continue == b'1'):
        filesize = os.path.getsize('Videos\\Pan-Se-Cae2video.mp4')
        s.send(filesize.to_bytes(8, 'little'))
        for b in f:
            b_array.append(b)
            s.send(b)
    else:
        s.close()

        
if __name__ == "__main__":
    main('localhost', 2000)