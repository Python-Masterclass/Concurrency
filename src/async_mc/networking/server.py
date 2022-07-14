import asyncio
import logging
import selectors
import signal
import socket


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


def fib_handler(sock):
    try:
        req = sock.recv(100).strip()
    except BlockingIOError:
        pass
    else:
        if req:
            n = int(req)
            result = fib(n)
            resp = f"{result}\n".encode("utf-8")
            sock.send(resp)


def fib_server_non_blocking(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)   # This is new!
    selector = selectors.DefaultSelector()
    selector.register(sock, selectors.EVENT_READ)

    while True:
        events = selector.select(timeout=1)
        for event, _ in events:
            event_socket = event.fileobj
            if event_socket == sock:
                client, addr = sock.accept()
                client.setblocking(False)
                print(f"Connection from {addr}")
                selector.register(client, selectors.EVENT_READ)
            else:
                fib_handler(event_socket)


async def fib_handler_async(sock, loop):
    try:
        while req := await loop.sock_recv(sock, 100):
            n = int(req.strip())
            result = fib(n)
            resp = f"{result}\n".encode("utf-8")
            await loop.sock_sendall(sock, resp)
    except ConnectionResetError:
        pass
    except Exception as ex:
        logging.exception(ex)
    finally:
        sock.close()


async def wait_for_connection(sock, loop):
    while True:
        client, addr = await loop.sock_accept(sock)
        client.setblocking(False)
        print(f"Connection from {addr}")
        asyncio.create_task(fib_handler_async(client, loop))


def cancel_tasks():
    print(f"Canceling tasks")
    try:
        for task in asyncio.all_tasks():
            task.cancel()
    except RuntimeError:
        pass


async def fib_server_async(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)   # This is new!
    selector = selectors.DefaultSelector()
    selector.register(sock, selectors.EVENT_READ)
    loop = asyncio.get_event_loop()
    # loop.add_signal_handler(signal.SIGINT, cancel_tasks)  # Does not work on Windows
    await wait_for_connection(sock, loop)

    while True:
        events = selector.select(timeout=1)
        for event, _ in events:
            event_socket = event.fileobj
            if event_socket == sock:
                client, addr = sock.accept()
                client.setblocking(False)
                print(f"Connection from {addr}")
                selector.register(client, selectors.EVENT_READ)
            else:
                fib_handler_async(event_socket)


if __name__ == "__main__":
    address = ("", 25000)
    # fib_server(address)
    # fib_server_non_blocking(address)
    try:
        asyncio.run(fib_server_async(address))
    except KeyboardInterrupt:
        cancel_tasks()
