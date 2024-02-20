import os
import socket
import logging
import choice
import configparser

logger = logging.getLogger('client-info')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class User:
	username: str
	sock: socket.socket

	def __init__(self, _socket, _username=os.getlogin(), password_hash=None):
		self.sock = _socket
		self.username = _username

	def __pre_login(self):
		pass

	def handle_login(self):
		self.pre_login()


def pre_connect():
	if os.path.isfile(config_file):
		config = configparser.ConfigParser()
		config.read(config_file)
		return ["connection.details"]["IpAddress"], config["connection.details"]["Port"]
	return  choice.input("IP address to connect to: "), choice.input("Port of the address: ")

# add connection retries.
def connect(ip, port, mode="nogui") -> socket.socket:
	"""
	Connects client to specified ip and port using TCP and IPv4.
	"""

	_client = socket.socket(family=socket.AF_INET, proto=socket.IPPROTO_TCP)
	_client.connect((ip, port))
	return _client


if __name__ == "__main__":
	print(f"Currently using username: {os.getlogin()}")
	choices: list = ["Connect to server", "Change username"]
	config_file = "config.cfg"

	match choice.Menu(choices, title="Action menu:").ask():
		case "Connect to server":
			ip, port = pre_connect()

	client: User = User(connect(ip, port))
	client.handle_login(client)
