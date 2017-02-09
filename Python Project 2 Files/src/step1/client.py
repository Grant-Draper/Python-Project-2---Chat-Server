import socket
from message import *

# sever address to connect to
server_ip_address = '127.0.0.1'
server_port = 5000

# message types
NORMAL = 0


# 1. create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. connect the socket object to the server's ip address and port
server_socket.connect((server_ip_address, server_port))

while(True):
	# 3. get a message from the user
	msg_text = raw_input('> ') 	# 5. remove


	# 4. send a message of type NORMAL, with this message, to the server
	send_msg(NORMAL, msg_text, server_socket) # 6. remove


	# 7. check if input has been received from stdin or the server_socket
	# 8. if sys.stdin is available to read, read from it and send the message
	# 9. if the server socket is available to read, read from it and print the message
