"""**********************************************************
        Grant Draper SFC5 - Chat Server (Client)
                    Chatterbox
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

    """Class called "Client", this contains a list of functions that can be
                executed to manage the Chatterbox Client."""

    server_details = []
    server_details_alt = []
    current_server = 0  # 0 = Not connected, 1 = HOST+PORT1, 2 = HOST+PORT2
    sockets = []
    current_user = "Not Logged In"
    chatroom = "Not In Chatroom"

    INITIAL_OPTIONS = ["1:     Log In",
                       "2:     Create New Account"]

    MAIN_MENU = ["1:    Chatrooms",
                 "2:    Friends",
                 "3:    Server Information \n",
                 "4:    Return to Current Chatroom",
                 "5:    Log Out"]

    CHATROOM_MENU = ["1:    View Available Chatrooms",
                     "2:    Join Chatroom",
                     "3:    Create Chatroom \n",
                     "4:    Return to Current Chatroom",
                     "5:    Main Menu"]

    FRIENDS_MENU = ["1:     View Friends",
                    "2:     Message Friend",
                    "3:     Add Friend",
                    "4:     Remove Friend \n",
                    "5:     Return to Current Chatroom",
                    "6:     Main Menu"]

    SERVER_INFO_MENU = ["1:      Uptime",
                        "2:      Total Number of Registered Users",
                        "3:      Total Number of Chatrooms \n",
                        "4:      Return to Current Chatroom",
                        "5:      Main Menu"]

    PRIVATE_CHAT_OPTIONS = ["1:     Accept Invitation",
                            "2:     Decline Invitation"]

    def __init__(self, HOST1, PORT1, HOST2, PORT2):

        """Initialisation function to open a socket when the client is started,
        this is then SSL encrypted. The Client will then attempt to connect to the first
        server, filing that will connect to the alternate. Then adds the socket to the
        client sockets list, then saves both server details seperately."""

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssl_socket = ssl.wrap_socket(server_socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
            try:
                self.ssl_socket.connect((HOST1, PORT1))
                Client.current_server = 1
                print("Client started:", HOST1, PORT1)
            except Exception as e:

                self.ssl_socket.connect((HOST2, PORT2))
                Client.current_server = 2
                print("Client started:", HOST2, PORT2)

            Client.sockets.append(self.ssl_socket)
            Client.server_details = [HOST1, PORT1]
            Client.server_details_alt = [HOST2, PORT2]

        except Exception as e:
            print(e)
            print("Completed with Exception1.", "\n")
            pass

    def initial_options(self):

        """This function provides a simple, initial menu structure to allow a user
            to log in or create an account."""

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

        """This function is the data gathering that organises the collection of
            user information for account creation."""

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Create new account", "\n")

        fname = self.get_fname()[1]
        lname = self.get_lname()[1]
        sname = self.get_screenname()[1]
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

        """This function initiates the registration data collection, then sends the values
            to the server once completed."""

        user = Client.gather_user_details(self)
        msg.send_static_msg(Message.TYPES["COMMAND"], user, Client.sockets[-1])
        Client.partially_listening(self)

    def create_new_public_chatroom(self):

        """This function allows the User to create a new chatroom."""

        while True:
            print("Please type the chatroom name:")
            chatroom = input()
            print("Please type the chatroom description:")
            description = input()
            if len(chatroom) == 0:
                print("Chatroom name invalid")
                pass

            elif len(chatroom) <= 20 and chatroom.isalnum():
                msg.send_static_msg(Message.TYPES["COMMAND"], "53|" + chatroom + "|" + description, Client.sockets[-1])
                Client.partially_listening(self)



    def user_log_in(self):

        """This function controls the user log in screen, collecting the username and
            password, then sending it to the credential checker."""

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Log in page", "\n")

        user = self.get_screenname()
        pswd = self.get_pass()

        if user[0] is True and pswd[0] is True:
            self.check_credentials(user[1], pswd[1])

    def get_fname(self):

        """This function controls the gathering of the users first name."""

        while True:
            print("Please enter your firstname:")
            fname = input()
            if len(fname) == 0:
                print("Firstname invalid")
                pass

            elif len(fname) <= 30 and fname.isalnum():
                return True, str(fname)

    def get_lname(self):

        """This function controls the gathering of the users last name."""

        while True:
            print("Please enter your lastname:")
            lname = input()
            if len(lname) == 0:
                print("Lastname invalid")
                pass

            elif len(lname) <= 30 and lname.isalnum():
                return True, str(lname)

    def get_screenname(self):

        """This function controls the gathering of the users screen name."""

        while True:
            print("Please enter a username:")
            sname = input()
            if len(sname) == 0:
                print("Username invalid")
                pass

            elif len(sname) <= 20 and sname.isalnum():
                return True, str(sname)

    def get_pass(self):

        """This function controls the gathering of the users password, this value is
            sha3 512 hashed then passed on."""

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

        """This function controls sending the log in information to the server, and sets
            the current user value."""

        msg.send_static_msg(Message.TYPES["USER"], user, Client.sockets[-1])
        msg.send_static_msg(Message.TYPES["PASS"], pswd, Client.sockets[-1])

        Client.current_user = user
        Client.partially_listening(self)

    def main_menu(self, user):

        """This function controls the main menu screen, allowing the user to navigate the program."""

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
        if selection == 4:  # Return to chat
            Client.return_to_chat(self)
            pass
        if selection == 5:  # Log Out
            Client.initial_options(self)
            pass

    def chatroom_menu(self):

        """This function controls the chatroom menu screen, allowing the user to navigate the program."""

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
            Client.create_new_public_chatroom(self)
            pass
        if selection == 4:  # Return to chat
            Client.return_to_chat(self)
            pass
        if selection == 5:  # Main menu
            Client.main_menu(self, Client.current_user)
            pass

    def friends_menu(self):

        """This function controls the friends menu screen, allowing the user to navigate the program."""

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
            print("Function not yet operational")
            Client.friends_menu(self)
            pass
        if selection == 4:  # Remove
            print("Function not yet operational")
            Client.friends_menu(self)
            pass
        if selection == 5:  # Return to chat
            Client.return_to_chat(self)
            pass
        if selection == 6:  # Main menu
            Client.main_menu(self, Client.current_user)
            pass

    def server_menu(self):

        """This function controls the server menu screen, allowing the user to navigate the program."""

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Server Menu", "\n")

        for option in Client.SERVER_INFO_MENU:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.SERVER_INFO_MENU)

        if selection == 1:  # Uptime
            Client.get_server_uptime(self)
            pass
        if selection == 2:  # Users total
            Client.get_total_users(self)
            pass
        if selection == 3:  # Chatrooms total
            Client.get_total_chatrooms(self)
            pass
        if selection == 4:  # Return to chat
            Client.return_to_chat(self)
            pass
        if selection == 5:  # Main menu
            Client.main_menu(self, Client.current_user)
            pass

    def get_server_uptime(self):

        """Function to retrieve the servers uptime."""

        Message.send_static_msg(self, Message.TYPES["COMMAND"], "54", self.ssl_socket)
        Client.partially_listening(self)

    def get_total_users(self):

        """Function to retrieve the servers uptime."""

        Message.send_static_msg(self, Message.TYPES["COMMAND"], "55", self.ssl_socket)
        Client.partially_listening(self)

    def get_total_chatrooms(self):

        """Function to retrieve the servers uptime."""

        Message.send_static_msg(self, Message.TYPES["COMMAND"], "56", self.ssl_socket)
        Client.partially_listening(self)


    def return_to_chat(self):

        """This function allows a user to rejoin their current chat, or start the listening
            loop without being assigned to a chatroom."""

        if Client.chatroom == "Not In Chatroom":
            print("\n \n{0}, you have not joined a Chatroom.".format(Client.current_user))
            print("Type !QuiT! to exit.\n")
            Client.listening(self)
        else:
            Client.listening(self)

    def join_chatroom(self):

        """This function controls the join chatroom screen."""

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

        """This function controls the start private chat screen."""

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Start Private Chat", "\n")

        while True:
            print("{0}, please type the Screen Name of the friend you want to talk to:".format(Client.current_user))
            sname = input()
            if len(sname) == 0:
                print("Screen Name invalid")
                pass

            elif len(sname) <= 20 and sname.isalnum():
                Client.chatroom = "PRIVATE_ROOM-{0}".format(Client.current_user)
                msg.send_static_msg(Message.TYPES["DIRECT"], "41|" + Client.chatroom + "|" + sname, Client.sockets[-1])
                Client.partially_listening(self)
                return

    def private_chat_invitation(self):

        """This function controls how the user can respond to a private chat invitation."""

        for option in Client.PRIVATE_CHAT_OPTIONS:
            print(option)
        print("\n")

        selection = Client.option_input_valid(self, Client.SERVER_INFO_MENU)

        if selection == 1:  # Accept
            msg.send_static_msg(Message.TYPES["DIRECT"], "42|" + Client.chatroom, Client.sockets[-1])
            Client.listening(self)
            pass
        if selection == 2:  # Decline
            msg.send_static_msg(Message.TYPES["DIRECT"], "43|" + Client.chatroom, Client.sockets[-1])
            Client.chatroom = "Not In Chatroom"
            Client.main_menu(self, Client.current_user)
            pass

    def option_input_valid(self, list):

        """This function controls how the user can respond to a menu selections."""

        while True:
            selection = Client.input_only_int(self)
            if (selection - 1) in range(0, len(list)):
                return selection

    def input_only_int(self):

        """This function ensures that only integers can be entered."""

        selection = None
        while selection == None:
            try:
                print("Please select by typing the option number:")
                selection = int(input())

            except ValueError:
                print("Input invalid, please enter a valid option number")
        return selection

    def listening(self):

        """This function reads from both stdin and the socket using a select statement,
            this will send the message from stdin. from the socket it will receive and
            pass to the message filter."""

        while True:

            # check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([sys.stdin, self.ssl_socket], [], [], 1)
            try:
                # if sys.stdin is available to read, read from it and send the message
                if sys.stdin in available_streams:
                    msg_text = sys.stdin.readline()

                    if msg_text == "!QuiT!\n":
                        Message.send_static_msg(self, Message.TYPES["COMMAND"], msg_text + " " + Client.chatroom, self.ssl_socket)
                        Client.partially_listening(self)

                    if msg_text[0] == "/":
                        Message.send_static_msg(self, Message.TYPES["COMMAND"], (msg_text.replace("\n", "")) + " " + Client.chatroom, self.ssl_socket)

                    Message.send_msg(self, Message.TYPES["NORMAL"], msg_text, self.ssl_socket)
                    continue

                # if the server socket is available to read, read from it and pass to the filter
                if self.ssl_socket in available_streams:
                    msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                    Client.message_filter(self, msg_text, msg_type)

            except Exception as e:
                """This try catch will attempt to reconnect to an instance of the server if the connection fails."""
                print(e)
                if Client.current_server == 1:
                    Client.__init__(self, Client.server_details_alt[-2], Client.server_details_alt[-1], Client.server_details[-2], Client.server_details[-1])
                    Client.main_menu(self, Client.current_user)
                else:
                    Client.__init__(self, Client.server_details[-2], Client.server_details[-1], Client.server_details_alt[-2], Client.server_details_alt[-1])
                    Client.main_menu(self, Client.current_user)

    def partially_listening(self):

        """This function allows the client to wait for a response from the server, but removes user
            input by removing the read from stdin sections."""

        while True:
            # check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([self.ssl_socket], [], [], 1)

            # if the server socket is available to read, read from it and print the message
            if self.ssl_socket in available_streams:
                msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                Client.message_filter(self, msg_text, msg_type)

    def message_filter(self, msg_text, msg_type):

        """This function will process messages recieved and decide on an action depending on their
            type, the server will only send SERVER messages and NORMAL messages to a client."""

        msg_type = str(msg_type)

        if msg_type[0] == "0":  # NORMAL
            Client.ao_normal_msg(self, msg_text)

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

        """Function called "ActionsOn_normal_msg" this will format and print a NORMAL message type."""

        timestamp = datetime.now()
        print("({0}:{1}:{2})".format(timestamp.hour, timestamp.minute, timestamp.second), msg_text)
        return

    def ao_server_msg(self, msg_text, msg_type):

        """Function called "ActionsOn_server_msg" this provides further filtering for the SERVER
            message type, this allows the type to be split further into subtypes."""

        msg_type = str(msg_type)

        if len(msg_type) == 2:

            if msg_type == "61":                                 # "Login Successful."
                print("login ok")
                Client.main_menu(self, Client.current_user)

            elif msg_type == "62":                                # "Login Unsuccessful.":
                print("Authentication Failure, Login Unsuccessful.")
                Client.initial_options(self)

            elif msg_type == "63":                                   # "Username already in use.":
                print("Username already in use, please try again.")
                Client.create_new_user(self)

            elif msg_type == "64":                                  # "Account successfully registered.":
                print("Account Successfully registered.")
                Client.initial_options(self)

            elif msg_type == "65":                                  # "Chatroom does not exist.":
                print("Chatroom does not exist.")
                Client.chatroom_menu(self)

            elif msg_type == "66":                                   # "Joined the Chatroom.":
                print("Sucessfully joined Chatroom, please type !QuiT! to exit.")
                Client.listening(self)

            elif msg_type == "67":                                   # "User already in Chatroom.":
                print("User already in Chatroom")
                Client.main_menu(self, Client.current_user)

            elif msg_type == "68":                                   # "User removed from Chatroom.":
                print("User exited Chatroom.")
                Client.main_menu(self, Client.current_user)

            elif msg_type == "69":                                      # "Available Chatrooms.":
                print("\n")
                print("ChatterBox", "\n", "\n")
                print("Available Chatrooms.", "\n")
                print("Room Names: \n")
                rooms = msg_text.split("|")

                for room in rooms:
                    print(room)
                Client.chatroom_menu(self)

        elif len(msg_type) == 3:

            if msg_type == "610":                                        # "Online Users."
                print("\n")
                print("ChatterBox", "\n", "\n")
                print("Online Users.", "\n")
                print("User Names: \n")
                rooms = msg_text.split("|")

                for room in rooms:
                    print(room)
                Client.friends_menu(self)

            elif msg_type == "611":                                  # Sender: "You have successfully started a private chat."
                print(msg_text, ": Please wait for the other user to join, or type !QuiT! to exit.")
                Client.listening(self)

            elif msg_type == "612":                                   # Sender: "You have successfully left the chat."
                print(msg_text, ": You have successfully left the chat.")
                Client.main_menu(self, Client.current_user)

            elif msg_type == "613":                                    # Recipient: "User has left the chat."
                print(msg_text, ": Type !QuiT! to leave the Chatroom.")

            elif msg_type == "614":                                    # Recipient: "You have been invited to join a private chat."
                print(msg_text, ": You have been invited to join a private chat.")
                parts = msg_text.split(',')
                Client.chatroom = "PRIVATE_ROOM-{0}".format(parts[0])
                print(Client.chatroom)
                Client.private_chat_invitation(self)

            elif msg_type == "615":                                   # Sender: "Private chat invitation declined by recipient."
                print(msg_text, ": Private chat invitation declined by recipient.")
                Client.chatroom = "Not In Chatroom"
                Client.main_menu(self, Client.current_user)

            elif msg_type == "616":                                       # Recipient: "You have joined a private chat."
                print(msg_text, ": You have joined a private chat, type !QuiT! to exit.")
                Client.listening(self)

            elif msg_type == "617":                                       # Recipient: "You have been removed from the Chatroom."
                print(msg_text, ": You have been removed from the Chatroom, RESPECT THE RULES OR YOU WILL BE BANNED.")
                Client.main_menu(self, Client.current_user)
                Client.chatroom = "Not In Chatroom"

            elif msg_type == "618":                                       # Recipient: "Chatroom already exists"
                print(msg_text, ": Please try again.")
                Client.chatroom_menu(self)

            elif msg_type == "619":                                       # Recipient: "Chatroom created"
                print(msg_text, ": New Public Chatroom.")
                Client.chatroom_menu(self)

            elif msg_type == "620":                                       # Recipient: "Current Server running time."
                print("Current ChatterBox running time.")
                start_time, running_time = msg_text.split("|")
                print("Server was started: {0}".format(start_time))
                print("Server has been running for: {0}".format(running_time))
                Client.server_menu(self)

            elif msg_type == "621":                                       # Recipient: "All Current Server Users."
                print("Current Registered Users: {0}".format(msg_text))
                Client.server_menu(self)

            elif msg_type == "622":                                       # Recipient: "All Current Server Chatrooms."
                print("Total Live Chatrooms: {0}".format(msg_text))
                Client.server_menu(self)

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

        """This function is used to send messages when the input is Stdin.
            Stdin will put an invisible "new line" character at the end of
             the inputted string, this function accounts for that."""

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

        """This is used to send messages when the input is the input() function"""

        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
            msg_text.strip().encode("utf-8"))  # cut off a newline

        Client.raw_send(self, sock, len(full_msg), full_msg)


msg = Message()
