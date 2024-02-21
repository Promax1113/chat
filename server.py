import json
import socket
import asyncio
import logging
import configparser
import base64
import hashlib
from typing import Final

BUFSIZE: Final[int] = 4096

logger = logging.getLogger('server-info')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class Client:
    sock: socket.socket
    address: socket.AddressInfo

    def __init__(self, _socket: socket.socket):
        self.sock = _socket
        self.address = self.sock.getpeername()

    async def receive(self, decode: bool = True) -> bytes | str:
        message = await loop.sock_recv(self.sock, BUFSIZE)
        return message.decode() if decode else message
    
    async def send(self, message):
        message = message if type(message) == bytes else message.encode()
        await loop.sock_sendall(self.sock, message)
# Make it async
async def handle_client(client: Client):
    # Is already returned decoded!!
    data = await client.receive()
    client_info = json.loads(data)
    print(client_info)


async def await_connections(server: socket.socket):
    while True:
        client, addr = await loop.sock_accept(server)
        print(f"Incoming connection from {addr}")
        logger.info(f"Now handling client {addr[0]} on port {addr[1]}...")
        await asyncio.create_task(handle_client(Client(client)))


def setup(ip: str, port: int, mode="nogui") -> socket.socket:
    """Setups the server's Socket."""
    server = socket.socket(family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    test_sk = socket.socket(family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    logger.info("Started test socket. Now testing...")
    server.bind((ip, port))
    server.listen(5)
    test_sk.connect((ip, port))
    client, addr = server.accept()
    test_sk.sendall("200".encode())
    test_data = client.recv(4096)
    logger.info(f"Data sent: 200; Data received: {test_data}")
    if test_data.decode() == "200":

        if mode == "gui":
            # Setup PyQt GUI
            pass

        print(f"Server started! Listening on {ip}:{port}...")
        return server

    else:
        print("Pre-connection socket testing failed! Creating new one...")
        return setup(ip, port)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    loop = asyncio.new_event_loop()
    server: socket.socket = setup("127.0.0.1", 7754)
    loop.run_until_complete(await_connections(server))

    print("finish")
