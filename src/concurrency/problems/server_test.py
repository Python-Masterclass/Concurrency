import socket
from threading import Thread, Event


def echo_server(address, stop_event, server_initialized):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(0.5)
    sock.bind(address)
    server_initialized.set()
    while not stop_event.is_set():
        print("server waiting for input")
        try:
            msg, addr = sock.recvfrom(1024)
        except socket.timeout:
            pass
        else:
            print(f"server received '{msg}' from {addr}")
            sock.sendto(msg, addr)
            print(f"Server echoed message back")
    print("server stopped")


def main():
    stop_event = Event()
    server_initialized = Event()
    server_address = ("localhost", 30000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    t = Thread(target=echo_server, args=(server_address, stop_event, server_initialized))
    try:
        t.start()
        server_initialized.wait(0.2)
        client_socket.sendto(b"hallo", server_address)
        resp, server = client_socket.recvfrom(1024)
        print(f"Received '{resp}' from server on {server}")
    finally:
        stop_event.set()
    print("Waiting for server to finish")
    t.join()
    print("Server finished")



if __name__ == "__main__":
    main()
