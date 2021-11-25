import socket
import time

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 25000))
    while True:
        start = time.time()
        sock.send(b"30\n")
        resp = sock.recv(100)
        end = time.time()
        print(end - start)

