import socket
import time
from threading import Thread

count = 0


def monitor():
    global count
    while True:
        time.sleep(1)
        print(f"{count} request per second")
        count = 0


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 25000))

    monitor_thread = Thread(target=monitor)
    monitor_thread.start()

    while True:
        sock.send(b"1\n")
        resp = sock.recv(100)
        count += 1

