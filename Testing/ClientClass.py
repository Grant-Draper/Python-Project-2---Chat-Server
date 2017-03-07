"""**********************************************************
        Grant Draper SFC5 - Chat Server (Client)
                Script Pre-Requisites

            ****** Must be ran on Linux ******

                Python 3.6 Interpreter
                Modules: pypyodbc 1.3.4
**********************************************************"""

import socket
import select
import ssl
import sys
import struct
import hashlib
import getpass
from datetime import datetime


# Message format is:
#   4 bytes unsigned type
#   4 bytes unsigned length
#   Message data


class Client:
    server_details = []
    sockets = []
    current_user = None
    chatroom = None

    INITIAL_OPTIONS = ["1:     Log In",
                       "2:     Create New Account"]

    MAIN_MENU = ["1:    Chatrooms",
                 "2:    Friends",
                 "3:    Server Information \n",
                 "4:    Log Out"]

    CHATROOM_MENU = ["1:    View Available Chatrooms",
                     "2:    Join Chatroom",
                     "3:    Create Chatroom \n",
                     "4:    Main Menu"]

    FRIENDS_MENU = ["1:     View Friends",
                    "2:     Message Friend",
                    "3:     Add Friend",
                    "4:     Remove Friend \n",
                    "5:     Main Menu"]

    SERVER_INFO_MENU = ["1:      Uptime",
                        "2:      Total Number of Registered Users",
                        "3:      Total Number of Chatrooms \n",
                        "4:      Main Menu"]

    PRIVATE_CHAT_OPTIONS = ["1:     Accept Invitation",
                            "2:     Decline Invitation"]

    def __init__(self, HOST, PORT):

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssl_socket = ssl.wrap_socket(server_socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
            self.ssl_socket.connect((HOST, PORT))
            Client.sockets.append(self.ssl_socket)
            Client.server_details += HOST, PORT
        except Exception as e:
            print(e)
            print("Completed with Exception1.", "\n")
            pass

    def initial_options(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Initial menu", "\n")

        for option in Client.INITIAL_OPTIONS:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.INITIAL_OPTIONS)

        if selection == 1:  # Log In
            Client.user_log_in(self)
            pass
        if selection == 2:  # Create New Account
            Client.create_new_user(self)
            pass

    def gather_user_details(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Create new account", "\n")

        fname = self.get_fname()[1]
        lname = self.get_lname()[1]
        sname = self.get_username()[1]
        while True:
            print("Create password, min 8 characters, a-z, 0-9")
            pswd1 = self.get_pass()[1]
            print("Confirm password")
            pswd2 = self.get_pass()[1]

            if pswd1 == pswd2:

                return (fname + " " + lname + " " + sname + " " + pswd1)
            else:
                print("\nPassword mismatch")

    def create_new_user(self):

        user = Client.gather_user_details(self)
        print(user)

        msg.send_static_msg(Message.TYPES["COMMAND"], user, Client.sockets[-1])
        Client.partially_listening(self)

    def user_log_in(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Log in page", "\n")

        user = self.get_username()
        pswd = self.get_pass()

        if user[0] is True and pswd[0] is True:
            self.check_credentials(user[1], pswd[1])

    def get_fname(self):

        while True:
            print("Please enter your firstname:")
            fname = input()
            if len(fname) == 0:
                print("Firstname invalid")
                pass

            elif len(fname) <= 30 and fname.isalnum():
                return True, str(fname)

    def get_lname(self):

        while True:
            print("Please enter your lastname:")
            lname = input()
            if len(lname) == 0:
                print("Lastname invalid")
                pass

            elif len(lname) <= 30 and lname.isalnum():
                return True, str(lname)

    def get_username(self):

        while True:
            print("Please enter a username:")
            sname = input()
            if len(sname) == 0:
                print("Username invalid")
                pass

            elif len(sname) <= 20 and sname.isalnum():
                return True, str(sname)

    def get_pass(self):

        while True:
            print("Please enter password:")
            pswd = getpass.getpass()
            pswd = str(pswd)
            if len(pswd) <= 7:
                print("Password invalid")
                pass

            elif len(pswd) > 7 and len(pswd) <= 50:
                pswd = hashlib.sha3_512(pswd.encode("utf-8")).hexdigest()

                return True, str(pswd)

    def check_credentials(self, user, pswd):

        msg.send_static_msg(Message.TYPES["USER"], user, Client.sockets[-1])
        msg.send_static_msg(Message.TYPES["PASS"], pswd, Client.sockets[-1])

        Client.current_user = user
        Client.partially_listening(self)

    def main_menu(self, user):

        print("\n")
        print("Welcome to ChatterBox {0}".format(user), "\n", "\n")
        print("Main Menu", "\n")

        for option in Client.MAIN_MENU:
            print(option)

        print("\n")

        selection = Client.option_input_valid(self, Client.MAIN_MENU)

        if selection == 1:  # Chatrooms
            Client.chatroom_menu(self)
            pass
        if selection == 2:  # Friends
            Client.friends_menu(self)
            pass
        if selection == 3:  # Server Info
            Client.server_menu(self)
            pass
        if selection == 4:  # Log Out
            Client.initial_options(self)
            pass

    def chatroom_menu(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Chatroom Menu", "\n")

        for option in Client.CHATROOM_MENU:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.CHATROOM_MENU)

        if selection == 1:  # View Chatrooms
            Message.send_static_msg(self, Message.TYPES["COMMAND"], "51", self.ssl_socket)
            pass
        if selection == 2:  # Join a chatroom
            Client.join_chatroom(self)
            pass
        if selection == 3:  # Create a chatroom
            pass
        if selection == 4:  # Main menu
            Client.main_menu(self, Client.current_user)
            pass

    def friends_menu(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Friends Menu", "\n")

        for option in Client.FRIENDS_MENU:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.FRIENDS_MENU)

        if selection == 1:  # View
            Message.send_static_msg(self, Message.TYPES["COMMAND"], "52", self.ssl_socket)
            pass
        if selection == 2:  # Message
            Client.start_private_chat(self)
            pass
        if selection == 3:  # Add
            pass
        if selection == 4:  # Remove
            pass
        if selection == 5:  # Main menu
            Client.main_menu(self, Client.current_user)
            pass

    def server_menu(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Server Menu", "\n")

        for option in Client.SERVER_INFO_MENU:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.SERVER_INFO_MENU)

        if selection == 1:  # Uptime
            pass
        if selection == 2:  # Users total
            pass
        if selection == 3:  # Chatrooms total
            pass
        if selection == 4:  # Main menu
            Client.main_menu(self, Client.current_user)
            pass

    def join_chatroom(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Join Chatroom", "\n")

        while True:
            print("Please type the chatroom name:")
            chatroom = input()
            if len(chatroom) == 0:
                print("Chatroom invalid")
                pass

            elif len(chatroom) <= 20 and chatroom.isalnum():
                msg.send_static_msg(Message.TYPES["JOIN"], chatroom, Client.sockets[-1])
                Client.chatroom = chatroom
                Client.partially_listening(self)
                return

    def start_private_chat(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Start Private Chat", "\n")

        while True:
            print("Please type the Screen Name of the friend you want to talk to:")
            sname = input()
            if len(sname) == 0:
                print("Screen Name invalid")
                pass

            elif len(sname) <= 20 and sname.isalnum():
                msg.send_static_msg(Message.TYPES["DIRECT"], sname, Client.sockets[-1])
                Client.chatroom = "PRIVATE_ROOM-{0}".format(Client.current_user)
                Client.partially_listening(self)
                return

    def private_chat_invitation(self):

        """"""

        for option in Client.PRIVATE_CHAT_OPTIONS:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.SERVER_INFO_MENU)

        if selection == 1:  # Accept
            msg.send_static_msg(Message.TYPES["DIRECT"], "45", Client.sockets[-1])
            pass
        if selection == 2:  # Decline
            pass

    def option_input_valid(self, list):

        while True:
            selection = Client.input_only_int(self)
            if (selection - 1) in range(0, len(list)):
                return selection

    def input_only_int(self):

        selection = None
        while selection == None:
            try:
                print("Please select by typing the option number:")
                selection = int(input())

            except ValueError:
                print("Input invalid, please enter a valid option number")
        return selection

    def listening(self):

        while True:

            # 6. check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([sys.stdin, self.ssl_socket], [], [], 1)
            try:
                # 7. if sys.stdin is available to read, read from it and send the message
                if sys.stdin in available_streams:
                    msg_text = sys.stdin.readline()

                    if msg_text == "!QuiT!\n":
                        # Client.main_menu(self, Client.current_user)
                        Message.send_static_msg(self, Message.TYPES["COMMAND"], msg_text + " " + Client.chatroom,
                                                self.ssl_socket)
                        Client.partially_listening(self)

                    Message.send_msg(self, Message.TYPES["NORMAL"], msg_text, self.ssl_socket)
                    continue

                # 8. if the server socket is available to read, read from it and print the message
                if self.ssl_socket in available_streams:
                    msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                    Client.message_filter(self, msg_text, msg_type)

                    ### Remove this statement when chatrooms working
                    # Message.print_message(self, msg_type, msg_text)

            except Exception as e:
                print(e)
                Client.__init__(self, Client.server_details[-2], Client.server_details[-1])

    def partially_listening(self):

        """ """

        while True:

            # 6. check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([self.ssl_socket], [], [], 1)

            # 8. if the server socket is available to read, read from it and print the message
            if self.ssl_socket in available_streams:
                msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                Client.message_filter(self, msg_text, msg_type)

    def message_filter(self, msg_text, msg_type):

        """"""

        msg_type = str(msg_type)

        if msg_type[0] == "0":  # NORMAL
            Client.ao_normal_msg(self, msg_text)

        elif msg_type[0] == "1":  # JOIN
            Client.ao_join_msg(self, msg_text)

        elif msg_type[0] == "2":  # USER
            Client.ao_user_msg(self, msg_text)

        elif msg_type[0] == "3":  # PASS
            Client.ao_pass_msg(self, msg_text)

        elif msg_type[0] == "4":  # DIRECT
            Client.ao_direct_msg(self, msg_text)

        elif msg_type[0] == "5":  # COMMAND
            Client.ao_command_msg(self, msg_text)

        elif msg_type[0] == "6":  # SERVER
            Client.ao_server_msg(self, msg_text, msg_type)

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

    def raw_send(self, sock, length, data):
        """ This function sends raw data on a socket."""

        total_sent = 0

        while total_sent < length:
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket send failure")
            total_sent = total_sent + sent

    def ao_normal_msg(self, msg_text):

        """Function called "ActionsOn_normal_msg" """

        timestamp = datetime.now()

        print("({0}:{1}:{2})".format(timestamp.hour, timestamp.minute, timestamp.second), msg_text)

        return

    def ao_join_msg(self, msg_text):

        """Function called "ActionsOn_join_msg" """

        return

    def ao_user_msg(self, msg_text):

        """Function called "ActionsOn_user_msg" """

        return

    def ao_pass_msg(self, msg_text):

        """Function called "ActionsOn_pass_msg" """

        return

    def ao_direct_msg(self, msg_text):

        """Function called "ActionsOn_direct_msg" """

        return

    def ao_command_msg(self, msg_text):

        """Function called "ActionsOn_command_msg" """

        return

    def ao_server_msg(self, msg_text, msg_type):

        """Function called "ActionsOn_server_msg" """

        msg_type = str(msg_type)

        # print(Message.print_message(msg, 6, msg_text))

        if len(msg_type) == 2:

            if msg_type[0] == "6" and msg_type[1] == "1":  # "Login Successful."
                print("login ok")
                Client.main_menu(self, Client.current_user)

            elif msg_type[0] == "6" and msg_type[1] == "2":  # "Login Unsuccessful.":
                print("Authentication Failure, Login Unsuccessful.")
                Client.initial_options(self)

            elif msg_type[0] == "6" and msg_type[1] == "3":  # "Username already in use.":
                print("Username already in use, please try again.")
                Client.create_new_user(self)

            elif msg_type[0] == "6" and msg_type[1] == "4":  # "Account successfully registered.":
                print("Account Successfully registered.")
                Client.initial_options(self)

            elif msg_type[0] == "6" and msg_type[1] == "5":  # "Chatroom does not exist.":
                print("Chatroom does not exist.")
                Client.chatroom_menu(self)

            elif msg_type[0] == "6" and msg_type[1] == "6":  # "Joined the Chatroom.":
                print("Sucessfully joined Chatroom.")
                Client.listening(self)

            elif msg_type[0] == "6" and msg_type[1] == "7":  # "User already in Chatroom.":
                print("User already in Chatroom")
                Client.main_menu(self, Client.current_user)

            elif msg_type[0] == "6" and msg_type[1] == "8":  # "User removed from Chatroom.":
                print("User exited Chatroom.")
                Client.main_menu(self, Client.current_user)

            elif msg_type[0] == "6" and msg_type[1] == "9":  # "Available Chatrooms.":

                print("\n")
                print("ChatterBox", "\n", "\n")
                print("Available Chatrooms.", "\n")

                print("Room Names: \n")
                rooms = msg_text.split("|")

                for room in rooms:
                    print(room)
                Client.chatroom_menu(self)

        elif len(msg_type) == 3:

            if msg_type[0] == "6" and msg_type[1] == "1" and msg_type[2] == "0":  # "Online Users."

                print("\n")
                print("ChatterBox", "\n", "\n")
                print("Available Chatrooms.", "\n")

                print("Room Names: \n")
                rooms = msg_text.split("|")

                for room in rooms:
                    print(room)
                Client.friends_menu(self)

            elif msg_type[0] == "6" and msg_type[1] == "1" and msg_type[
                2] == "1":  # "You have successfully started a private chat."
                print(msg_text, ": Please wait for the other user to join.")
                Client.listening(self)

            elif msg_type[0] == "6" and msg_type[1] == "1" and msg_type[
                2] == "2":  # "You have successfully left the chat."
                print(msg_text, ": You have successfully left the chat.")
                Client.main_menu(self, Client.current_user)

            elif msg_type[0] == "6" and msg_type[1] == "1" and msg_type[2] == "3":  # "User has left the chat."
                print(msg_text, ": Type !QuiT! to leave the Chatroom.")

            elif msg_type[0] == "6" and msg_type[1] == "1" and msg_type[
                2] == "4":  # "You have been invited to join a private chat."
                print(msg_text, ": You have been invited to join a private chat.")


class Message:
    TYPES = {"NORMAL": 0,  # 0
             "JOIN": 1,  # 1
             "USER": 2,  # 2
             "PASS": 3,  # 3
             "DIRECT": 4,  # 4
             "COMMAND": 5,  # 5
             "SERVER": 6}  # 6
    HEADER_LENGTH = 8

    def __init__(self):
        pass

    def send_msg(self, msg_type, msg_text, sock):
        """This function sends a message to a socket."""

        full_msg = struct.pack('!LL', msg_type, len(msg_text) - 1) + bytes(
            msg_text.strip().encode("utf-8"))  # cut off a newline

        Client.raw_send(self, sock, len(full_msg), full_msg)

    def receive_msg_from(self, sock):
        """This function waits for a message on a socket and returns the message type and text."""

        header = Client.raw_receive(self, sock, Message.HEADER_LENGTH)
        (msg_type, msg_length) = struct.unpack('!LL', header)

        try:
            msg_text = Client.raw_receive(self, sock, msg_length).decode("utf-8")
            return msg_type, msg_text

        except MemoryError as err:
            print("MemoryError: " + err.message)
            return None

    def print_message(self, msg_type, msg_text):
        """This function prints a message with the text length in a nice format."""

        msg_type = int(str(msg_type)[0])

        print((next(iter({k for k, v in Message.TYPES.items() if v == msg_type}))), len(msg_text), msg_text)

    def send_static_msg(self, msg_type, msg_text, sock):
        """."""

        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
            msg_text.strip().encode("utf-8"))  # cut off a newline

        Client.raw_send(self, sock, len(full_msg), full_msg)


msg = Message()

