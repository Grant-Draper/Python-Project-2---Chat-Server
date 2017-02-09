import socket
# import select
from message import *


# our address (we are the server)
server_ip_address = '127.0.0.1'
server_port = 5000

# 1. create a socket object
listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. bind to our own ip address and port
listening_socket.bind((server_ip_address, server_port))

# 3. start listening on the socket
listening_socket.listen(1)

# 4. accept a new connection
client_socket, client_address = listening_socket.accept() # 5. remove -- now accepting multiple clients

# 6. create an empty list to store the client sockets that connect

while(True):
	# 5. receive messages from the client
	(msg_type, msg_text) = receive_msg_from(client_socket) 	# 7. remove this

	# 6. print this message
	print_message(msg_type, msg_text) # 8. remove this



	# 9. select the sockets which have received input, timing out after 1 second

	# 10. loop through all the readable sockets

		# 11. if the socket is the our own, accept a client
		# (ie. use and write the accept_new_client_connection function below)

		# 12. else the socket is a client, so recieve the message and send it to everyone
		# (ie. use and write the receive_and_broadcast_message function below)



# starting solutions to 11, 12
# these defintions will need to be placed *before* you use them

# def accept_new_client_connection(listening_socket, client_sockets):
#	""" accept a connection from a client and append it to the client_sockets list """
#

# def receive_and_broadcast_message(readable_socket, client_sockets):
#	""" receive message from readable_socket and send it to all sockets in client_sockets """
#
