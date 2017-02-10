import socket
import select
from message import *


def accept_new_client_connection(listening_socket, client_sockets):
    """ accept a connection from a client and append it to the client_sockets list """
    # accept the new connection
    client_socket, client_address = listening_socket.accept()

    # add the new client to our list of clients
    client_sockets.append(client_socket)

    return client_sockets


def receive_and_broadcast_message(readable_socket, client_sockets):
    """ receive message from readable_socket and send it to all sockets in client_sockets """

    (msg_type, msg_text) = receive_msg_from(readable_socket)

    print_message(msg_type, msg_text)

    # if this message is a normal message, send it to all clients.
    # for now this includes the client that sent it in the first place.
    if msg_type == NORMAL:
        for client_socket in client_sockets:
            send_msg(msg_type, msg_text, client_socket)


# our address (we are the server)
server_ip_address = '127.0.0.1'
server_port = 5000

# 1. create a socket object
listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. bind to our own ip address and port
listening_socket.bind((server_ip_address, server_port))

# 3. start listening on the socket
listening_socket.listen(1)

# 6. create an empty list to store the client sockets that connect
client_sockets = []

while (True):
    # 9. select the sockets which have received input, timing out after 1 second
    readable_sockets, _, _ = select.select([listening_socket] + client_sockets, [], [], 1)

    # 10. loop through all the readable sockets
    for readable_socket in readable_sockets:

        # 11. if the socket is the our own, accept a client
        if readable_socket == listening_socket:
            # input has been received on the listening port.
            client_sockets = accept_new_client_connection(listening_socket, client_sockets)

        # 12. else the socket is a client, so recieve the message and send it to everyone
        else:
            # input has been received from an existing client
            receive_and_broadcast_message(readable_socket, client_sockets)
