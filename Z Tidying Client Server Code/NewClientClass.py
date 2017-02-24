import socket
import select
import ssl
import sys
import struct
import hashlib


# Message format is:
#   4 bytes unsigned type
#   4 bytes unsigned length
#   Message data


class Client:
    server_details = []
    sockets = []

    INITIAL_OPTIONS = ["1:     Log In",
                       "2:     Create New Account"]

    MAIN_MENU = ["1:    Chatrooms",
                 "2:    Friends",
                 "3:    Server Information",
                 "4:    Log Out"]

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

    def create_new_user(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Create new account", "\n")

        fname = self.get_fname()
        lname = self.get_lname()
        sname = self.get_username()
        pswd = None
        pswd1 = self.get_pass()
        pswd2 = self.get_pass()

        if pswd1 == pswd2:
            pswd = pswd1

        pass
        S

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
            user = input()
            if len(user) == 0:
                print("Firstname invalid")
                pass

            elif len(user) <= 30 and user.isalnum():
                return True, str(user)

    def get_lname(self):

        while True:
            print("Please enter your lastname:")
            user = input()
            if len(user) == 0:
                print("Lastname invalid")
                pass

            elif len(user) <= 30 and user.isalnum():
                return True, str(user)

    def get_username(self):

        while True:
            print("Please enter a Username:")
            user = input()
            if len(user) == 0:
                print("Username invalid")
                pass

            elif len(user) <= 20 and user.isalnum():
                return True, str(user)

    def get_pass(self):

        while True:
            print("Please enter a Password:")
            pswd = input()
            pswd = str(pswd)
            if len(pswd) <= 7:
                print("Password invalid")
                pass

            elif len(pswd) > 7 and len(pswd) <= 50:
                pswd = hashlib.sha3_512(pswd.encode("utf-8")).hexdigest()

                return True, str(pswd)

    def check_credentials(self, user, pswd):

        log_in_msg = Message()

        log_in_msg.send_static_msg(Message.TYPES["USER"], user, Client.sockets[-1])
        log_in_msg.send_static_msg(Message.TYPES["PASS"], pswd, Client.sockets[-1])

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

            pass
        if selection == 2:  # Friends
            pass
        if selection == 3:  # Server Info
            pass
        if selection == 4:  # Log Out
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
                    Message.send_msg(self, Message.TYPES["NORMAL"], msg_text, self.ssl_socket)
                    continue

                # 8. if the server socket is available to read, read from it and print the message
                if self.ssl_socket in available_streams:
                    msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                    Message.print_message(self, msg_type, msg_text)

            except Exception as e:
                Client.__init__(self, Client.server_details[-2], Client.server_details[-1])

    def partially_listening(self):

        """ Need to create a filter to act on different message types sent back by the server
            this needs to only listen to the select statement, not stdin. if you start the
            listening loop then you cannot exit from it, at the moment, possibly need an escape
            sequence.

            this filter should match a type then perform a specific output, and eventually restart
            the listening loop.

            need to redesign the database as the relationships are wrong at the moment,
            need to add extra entitys for expansion, see paper notes.

            also need to input test data into the database before upsize, this will allow proper
            testing of the select, update and removal statments."""

        while True:

            # 6. check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([self.ssl_socket], [], [], 1)

            # 8. if the server socket is available to read, read from it and print the message
            if self.ssl_socket in available_streams:

                msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)

                if msg_type == 0:  # NORMAL
                    Message.ao_normal_msg(msg, msg_text)

                    # Message.print_message(self, msg_type, msg_text)
                    # print(msg_type, msg_text)
                    break

                elif msg_type == 1:  # JOIN
                    Message.ao_join_msg(msg, msg_text)
                    break

                elif msg_type == 2:  # USER
                    Message.ao_user_msg(msg, msg_text)

                    # Message.print_message(self, msg_type, msg_text)
                    # print(msg_type, msg_text)
                    break

                elif msg_type == 3:  # PASS
                    Message.ao_pass_msg(msg, msg_text)
                    break

                elif msg_type == 4:  # DIRECT
                    Message.ao_direct_msg(msg, msg_text)
                    break

                elif msg_type == 5:  # COMMAND
                    Message.ao_command_msg(msg, msg_text)
                    break

                elif msg_type == 6:  # SERVER
                    Message.ao_server_msg(msg, msg_text)

                    # Message.print_message(self, msg_type, msg_text)
                    # Client.partially_listening(self)
                    break

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

        print((next(iter({k for k, v in Message.TYPES.items() if v == msg_type}))), len(msg_text), msg_text)

    def send_static_msg(self, msg_type, msg_text, sock):
        """This function sends a message to a socket."""

        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
            msg_text.strip().encode("utf-8"))  # cut off a newline

        Client.raw_send(self, sock, len(full_msg), full_msg)

    def ao_normal_msg(self, msg_text):

        """Function called "ActionsOn_normal_msg" """

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

    def ao_server_msg(self, msg_text):

        """Function called "ActionsOn_server_msg" """

        # print(Message.print_message(self, 6, msg_text))

        if msg_text == "Login Successful.":
            print("login ok")

        elif msg_text == "Login Unsuccessful.":
            print("no login")

        return


msg = Message()
import socket
import select
import ssl
import sys
import struct
import hashlib


# Message format is:
#   4 bytes unsigned type
#   4 bytes unsigned length
#   Message data


class Client:
    server_details = []
    sockets = []

    INITIAL_OPTIONS = ["1:     Log In",
                       "2:     Create New Account"]

    MAIN_MENU = ["1:    Chatrooms",
                 "2:    Friends",
                 "3:    Server Information",
                 "4:    Log Out"]

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

    def create_new_user(self):

        print("\n")
        print("ChatterBox", "\n", "\n")
        print("Create new account", "\n")

        fname = self.get_fname()
        lname = self.get_lname()
        sname = self.get_username()
        pswd = None
        pswd1 = self.get_pass()
        pswd2 = self.get_pass()

        if pswd1 == pswd2:
            pswd = pswd1

        pass
        S

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
            user = input()
            if len(user) == 0:
                print("Firstname invalid")
                pass

            elif len(user) <= 30 and user.isalnum():
                return True, str(user)

    def get_lname(self):

        while True:
            print("Please enter your lastname:")
            user = input()
            if len(user) == 0:
                print("Lastname invalid")
                pass

            elif len(user) <= 30 and user.isalnum():
                return True, str(user)

    def get_username(self):

        while True:
            print("Please enter a Username:")
            user = input()
            if len(user) == 0:
                print("Username invalid")
                pass

            elif len(user) <= 20 and user.isalnum():
                return True, str(user)

    def get_pass(self):

        while True:
            print("Please enter a Password:")
            pswd = input()
            pswd = str(pswd)
            if len(pswd) <= 7:
                print("Password invalid")
                pass

            elif len(pswd) > 7 and len(pswd) <= 50:
                pswd = hashlib.sha3_512(pswd.encode("utf-8")).hexdigest()

                return True, str(pswd)

    def check_credentials(self, user, pswd):

        log_in_msg = Message()

        log_in_msg.send_static_msg(Message.TYPES["USER"], user, Client.sockets[-1])
        log_in_msg.send_static_msg(Message.TYPES["PASS"], pswd, Client.sockets[-1])

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

            pass
        if selection == 2:  # Friends
            pass
        if selection == 3:  # Server Info
            pass
        if selection == 4:  # Log Out
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
                    Message.send_msg(self, Message.TYPES["NORMAL"], msg_text, self.ssl_socket)
                    continue

                # 8. if the server socket is available to read, read from it and print the message
                if self.ssl_socket in available_streams:
                    msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                    Message.print_message(self, msg_type, msg_text)

            except Exception as e:
                Client.__init__(self, Client.server_details[-2], Client.server_details[-1])

    def partially_listening(self):

        """ Need to create a filter to act on different message types sent back by the server
            this needs to only listen to the select statement, not stdin. if you start the
            listening loop then you cannot exit from it, at the moment, possibly need an escape
            sequence.

            this filter should match a type then perform a specific output, and eventually restart
            the listening loop.

            need to redesign the database as the relationships are wrong at the moment,
            need to add extra entitys for expansion, see paper notes.

            also need to input test data into the database before upsize, this will allow proper
            testing of the select, update and removal statments."""

        while True:

            # 6. check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([self.ssl_socket], [], [], 1)

            # 8. if the server socket is available to read, read from it and print the message
            if self.ssl_socket in available_streams:

                msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)

                if msg_type == 0:  # NORMAL
                    Message.ao_normal_msg(msg, msg_text)

                    # Message.print_message(self, msg_type, msg_text)
                    # print(msg_type, msg_text)
                    break

                elif msg_type == 1:  # JOIN
                    Message.ao_join_msg(msg, msg_text)
                    break

                elif msg_type == 2:  # USER
                    Message.ao_user_msg(msg, msg_text)

                    # Message.print_message(self, msg_type, msg_text)
                    # print(msg_type, msg_text)
                    break

                elif msg_type == 3:  # PASS
                    Message.ao_pass_msg(msg, msg_text)
                    break

                elif msg_type == 4:  # DIRECT
                    Message.ao_direct_msg(msg, msg_text)
                    break

                elif msg_type == 5:  # COMMAND
                    Message.ao_command_msg(msg, msg_text)
                    break

                elif msg_type == 6:  # SERVER
                    Message.ao_server_msg(msg, msg_text)

                    # Message.print_message(self, msg_type, msg_text)
                    # Client.partially_listening(self)
                    break

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

        print((next(iter({k for k, v in Message.TYPES.items() if v == msg_type}))), len(msg_text), msg_text)

    def send_static_msg(self, msg_type, msg_text, sock):
        """This function sends a message to a socket."""

        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
            msg_text.strip().encode("utf-8"))  # cut off a newline

        Client.raw_send(self, sock, len(full_msg), full_msg)

    def ao_normal_msg(self, msg_text):

        """Function called "ActionsOn_normal_msg" """

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

    def ao_server_msg(self, msg_text):

        """Function called "ActionsOn_server_msg" """

        # print(Message.print_message(self, 6, msg_text))
        import socket
        import select
        import ssl
        import sys
        import struct
        import hashlib

        # Message format is:
        #   4 bytes unsigned type
        #   4 bytes unsigned length
        #   Message data


        class Client:
            server_details = []
            sockets = []

            INITIAL_OPTIONS = ["1:     Log In",
                               "2:     Create New Account"]

            MAIN_MENU = ["1:    Chatrooms",
                         "2:    Friends",
                         "3:    Server Information",
                         "4:    Log Out"]

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

            def create_new_user(self):

                print("\n")
                print("ChatterBox", "\n", "\n")
                print("Create new account", "\n")

                fname = self.get_fname()
                lname = self.get_lname()
                sname = self.get_username()
                pswd = None
                pswd1 = self.get_pass()
                pswd2 = self.get_pass()

                if pswd1 == pswd2:
                    pswd = pswd1

                pass
                S

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
                    user = input()
                    if len(user) == 0:
                        print("Firstname invalid")
                        pass

                    elif len(user) <= 30 and user.isalnum():
                        return True, str(user)

            def get_lname(self):

                while True:
                    print("Please enter your lastname:")
                    user = input()
                    if len(user) == 0:
                        print("Lastname invalid")
                        pass

                    elif len(user) <= 30 and user.isalnum():
                        return True, str(user)

            def get_username(self):

                while True:
                    print("Please enter a Username:")
                    user = input()
                    if len(user) == 0:
                        print("Username invalid")
                        pass

                    elif len(user) <= 20 and user.isalnum():
                        return True, str(user)

            def get_pass(self):

                while True:
                    print("Please enter a Password:")
                    pswd = input()
                    pswd = str(pswd)
                    if len(pswd) <= 7:
                        print("Password invalid")
                        pass

                    elif len(pswd) > 7 and len(pswd) <= 50:
                        pswd = hashlib.sha3_512(pswd.encode("utf-8")).hexdigest()

                        return True, str(pswd)

            def check_credentials(self, user, pswd):

                log_in_msg = Message()

                log_in_msg.send_static_msg(Message.TYPES["USER"], user, Client.sockets[-1])
                log_in_msg.send_static_msg(Message.TYPES["PASS"], pswd, Client.sockets[-1])

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

                    pass
                if selection == 2:  # Friends
                    pass
                if selection == 3:  # Server Info
                    pass
                if selection == 4:  # Log Out
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
                            Message.send_msg(self, Message.TYPES["NORMAL"], msg_text, self.ssl_socket)
                            continue

                        # 8. if the server socket is available to read, read from it and print the message
                        if self.ssl_socket in available_streams:
                            msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
                            Message.print_message(self, msg_type, msg_text)

                    except Exception as e:
                        Client.__init__(self, Client.server_details[-2], Client.server_details[-1])

            def partially_listening(self):

                """ Need to create a filter to act on different message types sent back by the server
                    this needs to only listen to the select statement, not stdin. if you start the
                    listening loop then you cannot exit from it, at the moment, possibly need an escape
                    sequence.

                    this filter should match a type then perform a specific output, and eventually restart
                    the listening loop.

                    need to redesign the database as the relationships are wrong at the moment,
                    need to add extra entitys for expansion, see paper notes.

                    also need to input test data into the database before upsize, this will allow proper
                    testing of the select, update and removal statments."""

                while True:

                    # 6. check if input has been received from stdin or the server_socket
                    available_streams, _, _ = select.select([self.ssl_socket], [], [], 1)

                    # 8. if the server socket is available to read, read from it and print the message
                    if self.ssl_socket in available_streams:

                        msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)

                        if msg_type == 0:  # NORMAL
                            Message.ao_normal_msg(msg, msg_text)

                            # Message.print_message(self, msg_type, msg_text)
                            # print(msg_type, msg_text)
                            break

                        elif msg_type == 1:  # JOIN
                            Message.ao_join_msg(msg, msg_text)
                            break

                        elif msg_type == 2:  # USER
                            Message.ao_user_msg(msg, msg_text)

                            # Message.print_message(self, msg_type, msg_text)
                            # print(msg_type, msg_text)
                            break

                        elif msg_type == 3:  # PASS
                            Message.ao_pass_msg(msg, msg_text)
                            break

                        elif msg_type == 4:  # DIRECT
                            Message.ao_direct_msg(msg, msg_text)
                            break

                        elif msg_type == 5:  # COMMAND
                            Message.ao_command_msg(msg, msg_text)
                            break

                        elif msg_type == 6:  # SERVER
                            Message.ao_server_msg(msg, msg_text)

                            # Message.print_message(self, msg_type, msg_text)
                            # Client.partially_listening(self)
                            break

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

                print((next(iter({k for k, v in Message.TYPES.items() if v == msg_type}))), len(msg_text), msg_text)

            def send_static_msg(self, msg_type, msg_text, sock):
                """This function sends a message to a socket."""

                full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
                    msg_text.strip().encode("utf-8"))  # cut off a newline

                Client.raw_send(self, sock, len(full_msg), full_msg)

            def ao_normal_msg(self, msg_text):

                """Function called "ActionsOn_normal_msg" """

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

            def ao_server_msg(self, msg_text):

                """Function called "ActionsOn_server_msg" """

                # print(Message.print_message(self, 6, msg_text))

                if msg_text == "Login Successful.":
                    print("login ok")

                elif msg_text == "Login Unsuccessful.":
                    print("no login")

                return

        msg = Message()

        if msg_text == "Login Successful.":
            print("login ok")

        elif msg_text == "Login Unsuccessful.":
            print("no login")

        return


msg = Message()
