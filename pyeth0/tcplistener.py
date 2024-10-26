#  Copyright (c) 2024 Daniel Lima
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import socket
import threading


class TCPListener:

    def __init__(self, bind_ip: str = "0.0.0.0", port: int = 9999):
        self.bind_ip = bind_ip
        self.port = port

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.bind_ip, self.port))
            server.listen(5)
            print(f"[*] Listening on {self.bind_ip}:{self.port}")
            try:
                while True:
                    client, addr = server.accept()
                    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
                    handler = threading.Thread(
                        target=self.handle_client, args=(client,)
                    )
                    handler.start()
            except KeyboardInterrupt:
                print("[*] Shutting down server")
                server.close()

    @staticmethod
    def handle_client(client_socket: socket.socket):
        request = client_socket.recv(1024)
        print(f"[*] Received {request.decode()}")
        client_socket.send(b"ACK")
        client_socket.close()


if __name__ == "__main__":
    l = TCPListener()
    l.start_listening()
