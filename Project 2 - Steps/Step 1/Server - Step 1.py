import socket
from MessageStep1 import *

# our address (we are the server)
#HOST = "127.0.0.1"
HOST = "localhost"
PORT = 35000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()
print("connection from:", addr)



## creating a listening loop for the socket

def listening():

    while True:

        incoming_data = conn.recv(1024)

        if not incoming_data:
            continue
            #conn.shutdown(socket.SHUT_RDWR)
            #conn.close
            #server_socket.close()

        else:
            print('Received:', incoming_data)
            conn.sendall(incoming_data)



listening()










# 1. create a socket object

# 2. bind to our own ip address and port

# 3. start listening on the socket

# 4. accept a new connection

	#while(True):
		# 5. receive messages from the client
		# 6. print this message


# solution to (5)
# (msg_type, msg_text) = receive_msg_from(server_socket)

