from socketserver import TCPServer, StreamRequestHandler, ThreadingTCPServer

from concurrency.fibonacci import fib


class FibServer(ThreadingTCPServer):
    allow_reuse_address = True

    def server_bind(self):
        super().server_bind()
        print(f"Server listening on {self.server_address}")


class FibHandler(StreamRequestHandler):
    def handle(self):
        print(f"Connection from {self.client_address}")
        while req := self.request.recv(100).strip():
            n = int(req)
            result = fib(n)
            resp = str(result).encode('utf8') + b'\n'
            self.request.send(resp)
        print("Connection closed")


if __name__ == "__main__":
    with FibServer(("", 25000), FibHandler) as server:
        server.serve_forever()
