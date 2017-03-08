"""**********************************************************
        Grant Draper SFC5 - Chat Server (ServerClass)
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules: pypyodbc 1.3.4
**********************************************************"""

import socket
import ssl
import select
import struct
from datetime import datetime
from DatabaseClass1 import *


class Server:
    """Class called "Server", this contains a list of functions that can be
            executed to manage the Chat Server."""

    uptime_timestamp = None
    client_sockets = []
    user_logins = {}
    user_socket_pairs = {}
    private_client_link = {}

    def __init__(self, HOST, PORT):

        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master_socket.bind((HOST, PORT))
        self.master_socket.listen(1)
        self.uptime_timestamp = datetime.now()

    def accept_new_client_connection(self):

        """ Accept a connection from a client and append it to the client_sockets list """

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

    def write_to_logs(self, msg_type, msg_text, readable_socket):

        """ Function called 'write_to_logs', this checks first if the clients socket has
            already been tied to a user account. If it has then the username is provided
            for the Logs, if not (before log in stage), the log is assigned 'Unknown Client'."""

        if readable_socket in Server.user_socket_pairs.values():
            uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))
        else:
            uname = "Unknown Client"

        timestamp = str(datetime.now())
        d.write_to_logs_db(timestamp, uname, msg_type, msg_text, readable_socket)

    def receive_and_filter_message(self, readable_socket):

        """ Receive message from readable_socket, check the message type, start the
            relevant function to act on the message."""

        (msg_type, msg_text) = Message.receive_msg(msg, readable_socket)

        Server.write_to_logs(self, msg_type, msg_text, readable_socket)

        # Message.print_message(msg, msg_type, msg_text)

        if msg_type == 0:  # NORMAL
            Server.ao_normal_msg(self, msg_text, readable_socket)


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

        """This function receives length and bytes of raw data from a socket, returning the data."""

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
                        Server.receive_and_filter_message(self, readable_socket)

                    except Exception as e:
                        print(e)
                    continue

    def ao_normal_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_normal_msg", this extracts the username tied with
            with the socket object. It will then send the message to every active socket
            that has a username that is named in the Chatroom Users table.

            In short, sends the message to everyone in the same chatroom as the sender."""

        uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))

        for key in Server.user_socket_pairs.keys():
            if key != uname:

                if d.is_user_in_a_chatroom(key)[1] == d.is_user_in_a_chatroom(uname)[1]:
                    Message.send_msg(self, 0, "{0}: {1}".format(uname, msg_text), (next(iter(
                        {v for k, v in Server.user_socket_pairs.items() if k == key}))))


    def ao_join_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_join_msg", this retrieves the username tied with
            the socket object. It then checks if the user is already in the Chatroom,
            and notifies the user is they are. If not then it checks to see if the room
            exists, if so then the user will be added to the room, if not user is notified."""

        uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))

        while True:
            check = d.user_in_chatroom(uname, msg_text)

            if check[0] == False:
                value = d.add_user_to_chatroom(uname, msg_text)

                if value:
                    Message.send_msg(self, 66, msg_text, readable_socket)
                    return
                else:
                    Message.send_msg(self, 65, msg_text, readable_socket)
                    return
            else:
                d.remove_user_from_chatroom(uname, msg_text)

    def ao_user_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_user_msg", this checks to see if the user is already
            registered with the server, if not the user is notified. If they are registered,
            the username is temporarily added to storage with a timestamp, until reciept of
            the PASS message."""

        values = d.select_from_table_where("ScreenName", "Users", "ScreenName", msg_text)

        for value in values:
            if type(value[0]) == str:

                Server.user_logins[value[0]] = datetime.now()
                return True, "Username OK"
            else:
                msg.send_msg(63, "Login Unsuccessful.", readable_socket)

        return False, "Username not found"

    def ao_pass_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_pass_msg", this checks if the password hash matches one
            in the database and returns the screenname if it does. This screenname is then
            compared to the temporary screenname store, if it matches then the user has
            successfully authenticated. The temporary information is then deleted, after pairing
            a username to a socket in a dictionary."""

        returned_screenname = d.select_screenname_if_passhash_matches(msg_text)

        for value in returned_screenname:
            if type(value[0]) == str:

                if ('{0}'.format(value[0])) in Server.user_logins.keys():
                    msg.send_msg(61, "Login Successful.", readable_socket)
                    Server.user_socket_pairs[('{0}'.format(value[0].lower()))] = readable_socket

                    del Server.user_logins[value[0]]
                    return True, "Password OK"
            else:
                msg.send_msg(62, "Login Unsuccessful.", readable_socket)
        else:
            msg.send_msg(62, "Login Unsuccessful.", readable_socket)
        return False, "Login Unsuccessful."

    def ao_direct_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_direct_msg" """


        # Msg Format: type code | chatroom name | target screename - only for init msg
        parts = msg_text.split('|')
        sender_uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))

        if parts[0] == "41":  # Chat initiation message

            recipient_socket = (next(iter({v for k, v in Server.user_socket_pairs.items() if k == parts[2].lower()})))
            d.create_private_chat(sender_uname)

            if d.user_in_chatroom(sender_uname, parts[1])[0]:
                #Server.private_client_link[parts[2]] = readable_socket

                # Confirms to initiator
                msg.send_msg(611, "{0}, has started a private chat.".format(sender_uname), readable_socket)
                # Notifies the recipient
                msg.send_msg(614, "{0}, has started a private chat.".format(sender_uname), recipient_socket)
            else:
                print("about to join")
                x = d.join_private_chatroom(sender_uname, parts[1])
                print("after join results", x)
                #Server.private_client_link[parts[2]] = readable_socket
                msg.send_msg(611, "{0}, has started a private chat.".format(sender_uname), readable_socket)
                msg.send_msg(614, "{0}, has started a private chat.".format(sender_uname), recipient_socket)
            return

        elif parts[0] == "42":
            return

        elif parts[0] == "43":
            return

        elif parts[0] == "44":
            return

        elif parts[0] == "45":  # Accept chat invitation

            #partner_uname = (next(iter({k for k, v in Server.private_client_link.items() if v == sock})))
            d.join_private_chatroom(sender_uname, parts[1])
            msg.send_msg(616, "You have joined {0}.".format(parts[1]), readable_socket)
            return

        elif parts[0] == "46":
            partner_sock = (next(iter({v for k, v in Server.private_client_link.items() if k == partner_uname})))
            partner_uname = (next(iter({k for k, v in Server.private_client_link.items() if v == partner_sock})))
            del Server.user_logins[sender_uname]
            d.delete_chatroom(d.is_user_in_a_chatroom(partner_uname))
            msg.send_msg(615, "{0} has started a private chat.".format(partner_uname), partner_sock)
            return

        return

    def ao_command_msg(self, msg_text, readable_socket, msg_type):

        """Function called "ActionsOn_command_msg", the user can send different types of
            command message, this function filters these messages and performs the relevant
            actions. """

        msg_type = str(msg_type)

        if msg_text[0] == "!":
            """This acts on the escape sequence implemented in the client script. When
                this message is received, it retrieves the username paired with the socket. It
                then splits the message into its components (escape sequence, current chatroom),
                and removes the user from the chatroom, and notifies the user."""

            uname = (next(iter({k for k, v in Server.user_socket_pairs.items() if v == readable_socket})))
            parts = msg_text.split()

            if parts[1] == "PRIVATE_ROOM":
                check = d.is_user_in_a_chatroom(uname)
                if check[0]:
                    d.remove_user_from_chatroom()

                    msg.send_msg(611, "{0} has left the private chat.".format(uname), readable_socket)


            else:
                d.remove_user_from_chatroom(uname, parts[1])
                msg.send_msg(68, "User removed from Chatroom.", readable_socket)


        elif msg_text[0] == "5" and msg_text[1] == "1":
            """This allows the user to view all chatrooms, it retrieves all public
                chatrooms. This is then extracted and converted to a string with a delimiter
                added, this is then sent to the client."""

            room_string = ""
            rooms_description = d.view_all_chatrooms()

            for rooms in rooms_description:
                for room in rooms:
                    room_string += str(room) + "|"

            msg.send_msg(69, str(room_string), readable_socket)

        elif msg_text[0] == "5" and msg_text[1] == "2":
            """This allows the user to view all online users."""

            room_string = ""

            for key in Server.user_socket_pairs.keys():
                room_string += str(key) + "|"

            msg.send_msg(610, str(room_string), readable_socket)

        elif msg_type[0] == "5":
            """This allows a user to register with the server by starting the client
                registration function on receipt of the registration message."""
            Server.client_registration(self, msg_text, readable_socket)


        return

    def ao_server_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_server_msg"

            This could be used for cross-server communication, site transfers etc."""

        return

    def ao_temp_msg(self, msg_text, readable_socket):

        """Function called "ActionsOn_temp_msg" """

        return

    def client_registration(self, msg_text, readable_socket):

        """This function splits message into its components, it then checks if the screenname
            is already in use, if so the client is notified. If not the client details are
            inputted into the server and the account created, the user is then notified."""
        details = msg_text.split()

        returned_screenname = d.select_from_table_where("ScreenName", "Users", "ScreenName", details[2])

        if bool(returned_screenname) is False:
            d.create_new_user(details[0], details[1], details[2], details[3])
            msg.send_msg(64, "Account successfully registered.", readable_socket)

        else:
            msg.send_msg(63, "Username already in use.", readable_socket)
        return


class Message:
    """This class controls all the actions associated with messages, construction, printing and
        unpacking. The actual sending of the raw bytes is controlled by the server class."""

    TYPES = ["NORMAL",  # 0
             "JOIN",  # 1
             "USER",  # 2
             "PASS",  # 3
             "DIRECT",  # 4
             "COMMAND",  # 5
             "SERVER"]  # 6

    COMMAND_TYPES = ["CREATE_NEW_USER",  # 0
                     "VIEW_AVAILABLE_CHATROOMS",  # 1
                     "CREATE_NEW_CHATROOM",  # 2
                     "VIEW_FRIENDS",  # 3
                     "ADD_FRIEND",  # 4
                     "REMOVE_FRIEND",  # 5
                     "UPTIME",  # 6
                     "TOTAL_USERS",  # 7
                     "TOTAL_CHATROOMS"]  # 8

    HEADER_LENGTH = 8

    def __init__(self):
        pass

    def send_msg(self, msg_type, msg_text, sock):

        """This function sends a message to a socket, first writing the message to the server
            logs. This then constructs the header and passes it to the server to action the
            sending."""

        Server.write_to_logs(self, msg_type, msg_text, sock)

        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
            msg_text.strip().encode("utf-8"))
        Server.raw_send(self, sock, len(full_msg), full_msg)

    def receive_msg(self, sock):

        """This function waits for a message on a socket, unpacks the header and returns the
            message type and text."""

        header = Server.raw_receive(self, sock, Message.HEADER_LENGTH)
        (msg_type, msg_length) = struct.unpack('!LL', header)

        try:
            msg_text = Server.raw_receive(self, sock, msg_length).decode("utf-8")
            return msg_type, msg_text

        except MemoryError as err:
            print("MemoryError: " + err.message)
            return None

    def print_message(self, msg_type, msg_text):

        """This function prints a message with the type and text length."""

        print(Message.TYPES[msg_type], len(msg_text), msg_text)


d = Database()
msg = Message()



a = Server("192.168.1.201", 30000)

a.listening()