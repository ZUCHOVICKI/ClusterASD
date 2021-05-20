from socket import socket

def main():
    s = socket()
    s.connect(("localhost", 2000))

    f = open('Videos\\Pan-Se-Cae2video.mp4', 'rb')
    b_array = []

    s.send(b'{"type": "VIDEO", "message":"CONTINUE"}')
    # s.send(b'{"type": "NODE_CONNECT", "message": 9050}')

    should_continue = s.recv(1024)

    if(should_continue == b'1'):
        for b in f:
            b_array.append(b)
            s.send(b)
    else:
        s.close()

        
if __name__ == "__main__":
    main()