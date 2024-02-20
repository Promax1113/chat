import socket
import logging
import choices

logger = logging.getLogger('client-info')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


def pre_login(client: socket.socket):



def handle_login(client: socket.socket):
	pre_login(client)


# add connection retries.
def connect(ip, port, mode="nogui") -> socket.socket:
	"""
	Connects client to specified ip and port using TCP and IPv4.
	"""

	_client = socket.socket(family=socket.AF_INET, proto=socket.IPPROTO_TCP)
	_client.connect((ip, port))
	return _client


if __name__ == "__main__":
	client: socket.socket = connect("127.0.0.1", 7754)
	handle_login(client)
