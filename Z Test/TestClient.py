import socket
import select
import sys
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

while True:

    # 6. check if input has been received from stdin or the server_socket
    available_streams, _, _ = select.select([sys.stdin, server_socket], [], [], 1)

    # 7. if sys.stdin is available to read, read from it and send the message
    if sys.stdin in available_streams:
        msg_text = sys.stdin.readline()
        send_msg(NORMAL, msg_text, server_socket)

    # 8. if the server socket is available to read, read from it and print the message
    if server_socket in available_streams:
        (msg_type, msg_text) = receive_msg_from(server_socket)
