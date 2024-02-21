import json
import os
import socket
import asyncio
import logging
import configparser
import base64
import hashlib
from typing import Final
import choice
import fernet

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
        message = message if isinstance(message, bytes) else message.encode()
        await loop.sock_sendall(self.sock, message)


async def check_password(client_password, real_password):
    logger.info("Checking password provided...")
    if client_password == hashlib.sha256(real_password.encode()).hexdigest():
        return "200"
    return "401"


# Make it async
async def handle_client(client: Client):
    # Is already returned decoded!!
    data = await client.receive()
    client_info = json.loads(data)
    await client.send(await check_password(client_info["key_hash"], password))
    logger.info("Sent response!")


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
    config_file = "sconfig.cfg"
    config.read(config_file)
    if os.path.isfile(config_file) and "security" in config.sections():
        password = config["security"]['password']
    else:
        password = choice.Input("Enter the password for the server clients (20 char max)").ask()[:20]
        config["security"] = {'password': password}
        with open(config_file, "w") as f:
            config.write(f)

    loop = asyncio.new_event_loop()
    server: socket.socket = setup("127.0.0.1", 7754)
    loop.run_until_complete(await_connections(server))

    print("finish")
