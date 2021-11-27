import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 25000))
    print("Connected to server")
    while True:
        n = input().strip()  # Remove newline
        if not n:
            break
        sock.send(n.encode("utf-8"))
        response = sock.recv(100)
        print(f"{response.decode('utf-8').strip()}")


