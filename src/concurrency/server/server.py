import socket
import threading


def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def fib_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print(f"Connection from {addr}")
        fib_handler(client)


def fib_server_threaded(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=fib_handler, args=(client,)).start()


def fib_handler(sock):
    while True:
        req = sock.recv(100).strip()
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = f"{result}\n".encode("utf-8")
        sock.send(resp)


if __name__ == "__main__":
    address = ("", 25000)
    # fib_server(address)
    fib_server_threaded(address)
