
"""**********************************************************
        Grant Draper SFC5 - Chat Server (Client)
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules: pypyodbc 1.3.4
**********************************************************"""

import pypyodbc
import select
import socket
import ssl
import sys
import json
from MessageClass import *
from datetime import datetime


Host = "192.168.1.201"
Port = 30000
NORMAL = 0



def open_client_socket():#outgoing_data):

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_socket = ssl.wrap_socket(server_socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
        ssl_socket.connect((Host, Port))

    except Exception as e:
        print(e)
        print("Completed with Exception1.", "\n")
        pass

    while True:
        # 6. check if input has been received from stdin or the server_socket
        available_streams, _, _ = select.select([ssl_socket], [sys.stdin], [], 1)

        # 7. if sys.stdin is available to read, read from it and send the message
        if sys.stdin in available_streams:
            msg_text = sys.stdin.readline()
            Message.send_msg(NORMAL, msg_text, ssl_socket)
        continue

        # 8. if the server socket is available to read, read from it and print the message
        if ssl_socket in available_streams:
            msg_type, msg_text = Message.receive_msg_from(ssl_socket)
            #print(msg_text)
        continue




open_client_socket()

#Message.send_msg(NORMAL, "this is a test", ssl_socket)












    # try:
    #     # encodes the outgoing data in UTF-8 and writes it to the socket
    #     ssl_socket.write(outgoing_data.encode("UTF-8"))
    #
    #     # reads data from the socket and assigns it to a local variable
    #     incoming_data = ssl_socket.read()
    #
    #     # decodes the variable from UTF-8 and prints
    #     print(incoming_data.decode("UTF-8"))
    #
    #     # pauses the socket
    #     #ssl_socket.detach()
    #
    #     # closes the connection
    #     ssl_socket.close()
    #
    # except Exception as e:
    #     print(e)
    #     print("Completed with Exception2.", "\n")
    #     pass
    #     return




