
"""**********************************************************
        Grant Draper SFC5 - Chat Server (Server)
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules:
**********************************************************"""

import socket
import ssl
import json
import select
from MessageClass import *
from datetime import datetime


Host = ""
Port = 30000
client_sockets = []


def accept_new_client_connection(master_socket, client_sockets):

    """ accept a connection from a client and append it to the client_sockets list """

    # accept the new connection
    client_socket, client_address = master_socket.accept()

    # add the new client to our list of clients
    client_sockets.append(client_socket)

    ssl_socket = ssl.wrap_socket(client_socket, server_side=True, certfile="server.crt", keyfile="server.key")
    ssl_socket.setblocking(0)
    client_sockets.append(ssl_socket)


    return client_sockets


def receive_and_broadcast_message(readable_socket, client_sockets):
    """ receive message from readable_socket and send it to all sockets in client_sockets """

    (msg_type, msg_text) = Message.receive_msg_from(readable_socket)

    Message.print_message(msg_type, msg_text)

    # if this message is a normal message, send it to all clients.
    # for now this includes the client that sent it in the first place.
    if msg_type == 0:
    #if msg_type == NORMAL:
        for client_socket in client_sockets:
            Message.send_msg(msg_type, msg_text, client_socket)


#
# Host = ""
# Port = 30000


master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
master_socket.setblocking(0)
master_socket.bind((Host, Port))
master_socket.listen(1)

client_sockets = []

#client_sockets.append(master_socket)


def listening():

    while True:
        readable_sockets, _, _ = select.select([master_socket] + client_sockets, [], [], 1)# + client_sockets, [], [], 1)

        #(readable, writable, exceptional) = select.select(client_sockets, [], client_sockets)

        for readable_socket in readable_sockets:

            if readable_socket is master_socket:

                client_sockets.append(accept_new_client_connection(master_socket, client_sockets))
                pass


            else:

                receive_and_broadcast_message(readable_socket, client_sockets)
                continue

            """
                incoming_data = ssl_socket.read()

                if not incoming_data:
                    ssl_socket.shutdown(socket.SHUT_RDWR)
                    ssl_socket.close()
                    sockets.remove(ssl_socket)
                else:
                    decoded_data = incoming_data.decode("UTF-8")
                    python_data = json.loads(decoded_data)
                    outgoing_data = "Server Received Data"
                    ssl_socket.write(outgoing_data.encode("UTF-8"))

            """





listening()










