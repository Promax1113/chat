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
		client_data = {"username": self.username}

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
	choices: list = ["Connect to server", "Change username"]
	config_file = "config.cfg"
	config = configparser.ConfigParser()
	config.read(config_file)
	if os.path.isfile(config_file) and "user" in config.sections():
		username = config['user']['username']
	else:
		username = os.getlogin()
	ip, port = None, None
	while ip is None and port is None:
		print(f"\nCurrently using username: {username}\n")

		match choice.Menu(choices, title="Action menu:").ask():
			case "Connect to server":
				ip, port = pre_connect(config, config_file)

			case "Change username":
				username = choice.Input("New username (limit 12 char)").ask()[:12].replace(" ", "_")
				config['user'] = {'username': username}
				with open(config_file, "w") as file:
					config.write(file)
	client: User = User(connect(ip, int(port)), _username=username)
	client.handle_login()
