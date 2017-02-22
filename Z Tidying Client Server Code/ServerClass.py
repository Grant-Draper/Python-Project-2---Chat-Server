import socket
import ssl
import select
import struct
from datetime import datetime
from DatabaseClass import *


# HOST = "192.168.1.201"
# #HOST = "127.0.0.1"
# PORT = 30000

class Server:
    client_sockets = []
    user_logins = {}

    def __init__(self, HOST, PORT):

        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master_socket.bind((HOST, PORT))
        self.master_socket.listen(1)

    def start_master_socket(self):
        pass

    def accept_new_client_connection(self):  # , master_socket, client_sockets):
        """ accept a connection from a client and append it to the client_sockets list """
        try:
            # accept the new connection
            client_socket, client_address = self.master_socket.accept()

            # Wrap the socket with ssl
            ssl_socket = ssl.wrap_socket(client_socket, server_side=True, certfile="server.crt", keyfile="server.key")

            # Define blocking state
            ssl_socket.setblocking(0)

            # add the new client to our list of clients
            Server.client_sockets.append(ssl_socket)
        except Exception as e:
            print(e)

    def receive_and_broadcast_message(self, readable_socket, client_sockets):
        """ receive message from readable_socket and send it to all sockets in client_sockets """

        (msg_type, msg_text) = Message.receive_msg(self, readable_socket)

        Message.print_message(self, msg_type, msg_text)

        if msg_type == 0:  # NORMAL
            Message.ao_normal_msg(msg, msg_text, readable_socket)
            pass

        if msg_type == 1:  # JOIN
            Message.ao_join_msg(msg, msg_text, readable_socket)
            pass

        if msg_type == 2:  # USER
            Message.ao_user_msg(msg, msg_text, readable_socket)
            pass

        if msg_type == 3:  # PASS
            Message.ao_pass_msg(msg, msg_text, readable_socket)
            pass

        if msg_type == 4:  # DIRECT
            Message.ao_direct_msg(msg, msg_text, readable_socket)
            pass

        if msg_type == 5:  # COMMAND
            Message.ao_command_msg(msg, msg_text, readable_socket)
            pass

        if msg_type == 6:  # SERVER
            Message.ao_server_msg(msg, msg_text, readable_socket)
            pass

    def raw_receive(self, sock, length):
        """This function receives length bytes of raw data from a socket, returning the data."""

        chunks = []
        bytes_rx = 0

        try:
            while bytes_rx < length:
                chunk = sock.recv(length - bytes_rx)

                if chunk == b'':
                    raise RuntimeError("Socket connection broken")

                chunks.append(chunk)
                bytes_rx += len(chunk)

                return b''.join(chunks)

        except Exception as e:
            print(e)
            Server.client_sockets.remove(sock)

    def raw_send(self, sock, length, data):
        """ This function sends raw data on a socket."""

        total_sent = 0

        while total_sent < length:
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket send failure")
            total_sent = total_sent + sent

    def listening(self):

        """ Listening loop function to continually check the state of the sockets in the client_sockets
            list, and also accept new connections adding them to the list."""

        while True:

            readable_sockets, _, _ = select.select([self.master_socket] + Server.client_sockets, [], [], 1)

            for readable_socket in readable_sockets:

                if readable_socket == self.master_socket:

                    Server.accept_new_client_connection(self)

                    continue

                else:
                    try:
                        Server.receive_and_broadcast_message(self, readable_socket, Server.client_sockets)
                    except Exception as e:
                        print(e)
                    continue


class Message:
    TYPES = ["NORMAL",  # 0
             "JOIN",  # 1
             "USER",  # 2
             "PASS",  # 3
             "DIRECT",  # 4
             "COMMAND",  # 5
             "SERVER"]  # 6

    # TYPES = {"NORMAL": 0,  # 0
    #          "JOIN": 1,  # 1
    #          "USER": 2,  # 2
    #          "PASS": 3,  # 3
    #          "DIRECT": 4,  # 4
    #          "COMMAND": 5,  # 5
    #          "SERVER": 6}  # 6

    ## dictionary lookup string (next(iter({v for k, v in Message.TYPES.items() if k == "SERVER"})))

    HEADER_LENGTH = 8

    def __init__(self):
        pass

    def send_msg(self, msg_type, msg_text, sock):
        """This function sends a message to a socket."""

        # print("sending ", msg_text)

        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
            msg_text.strip().encode("utf-8"))  # cut off a newline
        Server.raw_send(self, sock, len(full_msg), full_msg)

    def receive_msg(self, sock):
        """This function waits for a message on a socket and returns the message type and text."""

        header = Server.raw_receive(self, sock, Message.HEADER_LENGTH)
        (msg_type, msg_length) = struct.unpack('!LL', header)

        try:
            msg_text = Server.raw_receive(self, sock, msg_length).decode("utf-8")
            return msg_type, msg_text

        except MemoryError as err:
            print("MemoryError: " + err.message)
            return None

    def print_message(self, msg_type, msg_text):
        """This function prints a message with the text length in a nice format."""

        print(Message.TYPES[msg_type], len(msg_text), msg_text)

    def ao_normal_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_normal_msg"
            if this message is a normal message, send it to all clients.
            this includes the client that sent it in the first place."""

        for client_socket in Server.client_sockets:
            # if client_socket is not readable_socket:
            Message.send_msg(self, 6, msg_text, client_socket)
        return

    def ao_join_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_join_msg" """

        return

    def ao_user_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_user_msg" """

        values = d.select_from_table_where("ScreenName", "Users", "ScreenName", msg_text)

        for value in values:
            if type(value[0]) == str:
                Server.user_logins[value[0]] = datetime.now()
                # msg.send_msg(6, "Username OK", readable_socket)

                return True, "Username OK"

        return False, "Username not found"

    def ao_pass_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_pass_msg" """

        """function working, now sending one message back to the client
            server message type, log in successful. no need to start on the
            next step of the client side user interaction, and the filtering
            from what happens after recieving server message 6. i think simmilar
            function layout to server, where it launches another function

            that function should filter by different server messages. potential
            to be big eventually"""

        returned_screenname = d.select_screenname_if_passhash_matches(msg_text)

        for value in returned_screenname:

            if type(value[0]) == str:
                if ('{0}'.format(value[0])) in Server.user_logins.keys():
                    msg.send_msg(6, "Log in successful.", readable_socket)
                    del Server.user_logins[value[0]]

                    return True, "Password OK"
        return False, "Username not found"

    def ao_direct_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_direct_msg" """

        return

    def ao_command_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_command_msg" """

        return

    def ao_server_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_server_msg" """

        return


d = Database()
msg = Message()