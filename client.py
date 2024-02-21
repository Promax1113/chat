import os
import socket
import logging
import choice
import configparser
from typing import Final
import hashlib
import json
import fernet

BUFSIZE: Final[int] = 4096

logger = logging.getLogger('client-info')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class User:
    username: str
    sock: socket.socket
    key: fernet.Fernet

    def __init__(self, _socket, _username=os.getlogin(), password_hash=None):
        self.sock = _socket
        self.username = _username

    @staticmethod
    def code2string(code: int) -> str:
        match int(code):
            case 200:
                return "Success!"
            case 401:
                return "Access denied!"
            case 500:
                return "Server error!"

    def __pre_login(self):
        client_data = {"username": self.username,
                       "key_hash": hashlib.sha256(choice.Input(
                           "Enter the password for the server connection (20 char max)").ask()[
                                                  :20].encode()).hexdigest()}

        self.send(json.dumps(client_data).encode())
        result = self.receive()
        print(self.code2string(result))

    def receive(self, decode: bool = True):
        message = None
        while message is None:
            message = self.sock.recv(BUFSIZE)
        return message.decode() if decode else message

    def send(self, message):
        message = message if isinstance(message, bytes) else message.encode()
        self.sock.sendall(message)

    def handle_login(self):
        self.__pre_login()


def pre_connect(config: configparser.ConfigParser, _config_file: str):
    config.read(_config_file)
    if os.path.exists(_config_file) and "connection.details" in config.sections():
        return config['connection.details']['ip_address'], config['connection.details']['port']
    _ip, _port = choice.Input("IP address to connect to").ask(), choice.Input("Port of the address", int).ask()
    config['connection.details'] = {'ip_address': _ip, 'port': _port}
    with open(_config_file, "w") as file:
        config.write(file)
    return _ip, _port


# add connection retries.
def connect(ip, port, mode="nogui") -> socket.socket:
    """
    Connects client to specified ip and port using TCP and IPv4.
    """
    print(f"Connecting to {ip}:{port}...")
    _client = socket.socket(family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    _client.connect((ip, port))
    return _client


if __name__ == "__main__":
    choices: list = ["Connect to server", "Change username", "Change saved IP Address"]
    config_file = "cconfig.cfg"
    config = configparser.ConfigParser()
    config.read(config_file)
    if os.path.isfile(config_file) and "user" in config.sections():
        username = config['user']['username']
        _ip, _port = config['connection.details']['ip_address'], config['connection.details']['port']
    else:
        username = os.getlogin()
    running = True
    while running:
        print(f"\nCurrently using username: {username}\n")
        print(f"IP and Port set to: {_ip}:{_port}" if _ip and _port else "No IP and Port set!")

        match choice.Menu(choices, title="Action menu:").ask():
            # !!! There is redundant code regarding IP and Port parsing from config.
            case "Connect to server":
                ip, port = pre_connect(config, config_file)
                running = False

            case "Change username":
                username = choice.Input("New username (limit 12 char)").ask()[:12].replace(" ", "_")
                config['user'] = {'username': username}
                with open(config_file, "w") as file:
                    config.write(file)
            case "Change saved IP Address":
                logger.info("Removing entry...")
                config.remove_section("connection.details")
                with open(config_file, "w") as f:
                    config.write(f)
                ip, port = pre_connect(config, config_file)
    client: User = User(connect(ip, int(port)), _username=username)
    client.handle_login()
