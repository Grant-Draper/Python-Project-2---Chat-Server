import socket
from MessageStep1 import *

# sever address to connect to
#HOST = "127.0.0.1"
HOST = "localhost"
PORT = 35000

# message types
NORMAL = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.sendall(bytes("Grant says hi again again", "utf8"))

while True:
    data = client_socket.recv(1024)
    print('Received', data)#repr(data))
    break

client_socket.shutdown(socket.SHUT_RDWR)
client_socket.close()





# 1. create a socket object

# 2. connect the socket object to the server's ip address and port

#while(True):
	# 3. get a message from the user

	# 4. create a message of type NORMAL with the string specified

	# 5. send this message to the server




# solution to (5)
# send_msg(NORMAL, msg_text, server_socket)
