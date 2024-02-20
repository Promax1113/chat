import socket
import asyncio
import logging

logger = logging.getLogger('server-info')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


# Make it async
async def handle_client(self: socket.socket):
    print(await loop.sock_recv(client, 4096))


async def await_connections(server: socket.socket):
    while True:
        client, addr = await loop.sock_accept(server)
        print(f"Incoming connection from {addr}")
        logger.info(f"Now handling self {addr[0]} on port {addr[1]}...")
        asyncio.create_task(handle_client(client))


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

        print("Server started!")
        return server

    else:
        print("Pre-connection socket testing failed! Creating new one...")
        return setup(ip, port)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    server: socket.socket = setup("127.0.0.1", 7754)
    loop.run_until_complete(await_connections(server))

    print("finish")
