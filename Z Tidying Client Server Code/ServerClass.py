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
    user_socket_pairs = {}

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

        (msg_type, msg_text) = Message.receive_msg(msg, readable_socket)

        Message.print_message(msg, msg_type, msg_text)

        if msg_type == 0:  # NORMAL
            Server.ao_normal_msg(self, msg_text, readable_socket)
            pass

        if msg_type == 1:  # JOIN
            Server.ao_join_msg(self, msg_text, readable_socket)
            pass

        if msg_type == 2:  # USER
            Server.ao_user_msg(self, msg_text, readable_socket)
            pass

        if msg_type == 3:  # PASS
            Server.ao_pass_msg(self, msg_text, readable_socket)
            pass

        if msg_type == 4:  # DIRECT
            Server.ao_direct_msg(self, msg_text, readable_socket)
            pass

        if msg_type == 5:  # COMMAND
            Server.ao_command_msg(self, msg_text, readable_socket, msg_type)
            pass

        if msg_type == 6:  # SERVER
            Server.ao_server_msg(self, msg_text, readable_socket)
            pass

        if msg_type == 7:  # TEMP
            Server.ao_temp_msg(self, msg_text, readable_socket)
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

    def ao_normal_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_normal_msg"
            if this message is a normal message, send it to all clients.
            this includes the client that sent it in the first place."""
        """
        for client_socket in Server.client_sockets:
            # if client_socket is not readable_socket:
            Message.send_msg(self, 6, msg_text, client_socket)
        return
        """

        uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))

        for key in Server.user_socket_pairs.keys():
            if key != uname:

                if d.is_user_in_chatroom(key)[1] == d.is_user_in_chatroom(uname)[1]:
                    Message.send_msg(self, 0, "{0}: {1}".format(uname, msg_text), (next(iter(
                        {v for k, v in Server.user_socket_pairs.items() if k == key}))))
            else:
                print("originator")






    def ao_join_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_join_msg" """

        uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))

        check = d.is_user_in_chatroom(uname)

        if check[0] is False:
            value = d.add_user_to_chatroom(uname, msg_text)

            if value[0]:
                Message.send_msg(self, 66, msg_text, readable_socket)
            else:
                Message.send_msg(self, 65, msg_text, readable_socket)
        else:
            Message.send_msg(self, 67, msg_text, readable_socket)
        return


    def ao_user_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_user_msg" """

        values = d.select_from_table_where("ScreenName", "Users", "ScreenName", msg_text)

        for value in values:
            if type(value[0]) == str:

                Server.user_logins[value[0]] = datetime.now()
                # msg.send_msg(6, "Username OK", readable_socket)
                return True, "Username OK"
            else:
                msg.send_msg(63, "Login Unsuccessful.", readable_socket)

        return False, "Username not found"

    def ao_pass_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_pass_msg" """

        returned_screenname = d.select_screenname_if_passhash_matches(msg_text)

        for value in returned_screenname:
            if type(value[0]) == str:

                if ('{0}'.format(value[0])) in Server.user_logins.keys():

                    msg.send_msg(61, "Login Successful.", readable_socket)
                    Server.user_socket_pairs[('{0}'.format(value[0]))] = readable_socket
                    #print(Server.user_socket_pairs)

                    del Server.user_logins[value[0]]

                    return True, "Password OK"
            else:
                msg.send_msg(62, "Login Unsuccessful.", readable_socket)
        else:
            msg.send_msg(62, "Login Unsuccessful.", readable_socket)

        return False, "Login Unsuccessful."

    def ao_direct_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_direct_msg" """

        return

    def ao_command_msg(self, msg_text, readable_socket, msg_type):

        """Function called "ActionsOn_command_msg" """

        msg_type = str(msg_type)

        if msg_text[0] == "!":
            uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))
            parts = msg_text.split()

            if d.remove_user_from_chatroom(uname, parts[1]):
                msg.send_msg(68, "User removed from Chatroom.", readable_socket)

        elif msg_type[0] == "5": # and msg_type[1] == "1":
            Server.client_registration(self, msg_text, readable_socket)
        return


    def ao_server_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_server_msg" """

        return

    def ao_temp_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_temp_msg" """

        return

    def client_registration(self, msg_text, readable_socket):

        details = msg_text.split()
        user_info = []

        returned_screenname = d.select_from_table_where("ScreenName", "Users", "ScreenName", details[2])

        if bool(returned_screenname) is False:
            d.create_new_user(details[0], details[1], details[2], details[3])
            msg.send_msg(64, "Account successfully registered.", readable_socket)

        else: #returned_screenname[0][0] == details[2]:
            msg.send_msg(63, "Username already in use.", readable_socket)
        return




class Message:
    TYPES = ["NORMAL",  # 0
             "JOIN",  # 1
             "USER",  # 2
             "PASS",  # 3
             "DIRECT",  # 4
             "COMMAND",  # 5
             "SERVER"]  # 6

    COMMAND_TYPES = ["CREATE_NEW_USER",             #0
                     "VIEW_AVAILABLE_CHATROOMS",    #1
                     "CREATE_NEW_CHATROOM",         #2
                     "VIEW_FRIENDS",                #3
                     "ADD_FRIEND",                  #4
                     "REMOVE_FRIEND",               #5
                     "UPTIME",                      #6
                     "TOTAL_USERS",                 #7
                     "TOTAL_CHATROOMS"]             #8


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


d = Database()
msg = Message()
