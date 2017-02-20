# import socket
# import select
# import ssl
# import sys
# import struct
#
#
# # Message format is:
# #   4 bytes unsigned type
# #   4 bytes unsigned length
# #   Message data
#
#
# class Client:
#     server_details = []
#     sockets = []
#
#     def __init__(self, HOST, PORT):
#
#         try:
#             server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.ssl_socket = ssl.wrap_socket(server_socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
#             self.ssl_socket.connect((HOST, PORT))
#             Client.sockets.append(self.ssl_socket)
#             Client.server_details += HOST, PORT
#
#         except Exception as e:
#             print(e)
#             print("Completed with Exception1.", "\n")
#             pass
#
#     def user_log_in(self):
#
#         """need to run the get uname and pass functions, then pass it through cred
#             checker, this will validate login, then can just print logged in.
#
#             something like, if Client.get_username()[0] == True and Client.get_pass()[0] == True
#                                 Client.cred_checker
#
#             see tictac toe"""
#
#         print("\n")
#         print("Welcome to ChatterBox", "\n", "\n")
#         print("Log in page")
#
#         user = self.get_username()
#         pswd = self.get_pass()
#
#         if user[0] is True and pswd[0] is True:
#             # print(user[1], pswd[1])
#             self.check_credentials(user[1], pswd[1])
#
#     def get_username(self):
#
#         while True:
#             print("Please enter a Username:")
#             user = input()
#             if len(user) == 0:
#                 print("Username invalid")
#                 pass
#
#             elif len(user) <= 20:
#                 print("ok")
#                 return True, str(user)
#
#     def get_pass(self):
#
#         while True:
#             print("Please enter a Password:")
#             pswd = input()
#             pswd = str(pswd)
#             if len(pswd) <= 7:
#                 print("Password invalid")
#                 pass
#
#             elif len(pswd) > 7 and len(pswd) <= 50:
#                 print("ok")
#                 return True, str(pswd)
#
#     def check_credentials(self, user, pswd):
#
#         log_in_msg = Message()
#
#         Message.send_static_msg(log_in_msg, Message.TYPES["USER"], user, Client.sockets[-1])
#         Client.partially_listening(self)
#
#
#         # print(self, Message.TYPES["USER"], user, self.ssl_socket)
#         # Message.send_msg(self, Message.TYPES["PASS"], pswd, self.ssl_socket)
#
#     def listening(self):
#
#         while True:
#
#             # 6. check if input has been received from stdin or the server_socket
#             available_streams, _, _ = select.select([sys.stdin, self.ssl_socket], [], [], 1)
#             try:
#                 # 7. if sys.stdin is available to read, read from it and send the message
#                 if sys.stdin in available_streams:
#                     msg_text = sys.stdin.readline()
#                     Message.send_msg(self, Message.TYPES["NORMAL"], msg_text, self.ssl_socket)
#                     continue
#
#                 # 8. if the server socket is available to read, read from it and print the message
#                 if self.ssl_socket in available_streams:
#                     msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
#                     Message.print_message(self, msg_type, msg_text)
#
#             except Exception as e:
#                 Client.__init__(self, Client.server_details[-2], Client.server_details[-1])
#
#     def partially_listening(self):
#
#         """ Need to create a filter to act on different message types sent back by the server
#             this needs to only listen to the select statement, not stdin. if you start the
#             listening loop then you cannot exit from it, at the moment, possibly need an escape
#             sequence.
#
#             this filter should match a type then perform a specific output, and eventually restart
#             the listening loop.
#
#             need to redesign the database as the relationships are wrong at the moment,
#             need to add extra entitys for expansion, see paper notes.
#
#             also need to input test data into the database before upsize, this will allow proper
#             testing of the select, update and removal statments."""
#
#
#         while True:
#
#             # 6. check if input has been received from stdin or the server_socket
#             available_streams, _, _ = select.select([self.ssl_socket], [], [], 1)
#
#             # 8. if the server socket is available to read, read from it and print the message
#             if self.ssl_socket in available_streams:
#
#                 msg_type, msg_text = Message.receive_msg_from(self, self.ssl_socket)
#
#                 if msg_type == 0:  # NORMAL
#                     break
#                 if msg_type == 1:  # JOIN
#                     break
#                 if msg_type == 2:  # USER
#                     Message.print_message(self, msg_type, msg_text)
#                     break
#                 if msg_type == 3:  # PASS
#                     break
#                 if msg_type == 4:  # DIRECT
#                     break
#                 if msg_type == 5:  # COMMAND
#                     break
#                 if msg_type == 6:  # SERVER
#                     break
#
#                     # Message.print_message(self, msg_type, msg_text)
#
#     def raw_receive(self, sock, length):
#         """This function receives length bytes of raw data from a socket, returning the data."""
#
#         chunks = []
#         bytes_rx = 0
#
#         try:
#             while bytes_rx < length:
#                 chunk = sock.recv(length - bytes_rx)
#                 if chunk == b'':
#                     raise RuntimeError("Socket connection broken")
#                 chunks.append(chunk)
#                 bytes_rx += len(chunk)
#             return b''.join(chunks)
#
#         except Exception as e:
#             print(e)
#
#     def raw_send(self, sock, length, data):
#         """ This function sends raw data on a socket."""
#
#         total_sent = 0
#
#         while total_sent < length:
#             sent = sock.send(data[total_sent:])
#             if sent == 0:
#                 raise RuntimeError("Socket send failure")
#             total_sent = total_sent + sent
#
#
# class Message:
#     TYPES = {"NORMAL": 0,  # 0
#              "JOIN": 1,  # 1
#              "USER": 2,  # 2
#              "PASS": 3,  # 3
#              "DIRECT": 4,  # 4
#              "COMMAND": 5,  # 5
#              "SERVER": 6}  # 6
#     HEADER_LENGTH = 8
#
#     def __init__(self):
#         pass
#
#     def send_msg(self, msg_type, msg_text, sock):
#         """This function sends a message to a socket."""
#
#         full_msg = struct.pack('!LL', msg_type, len(msg_text) - 1) + bytes(
#             msg_text.strip().encode("utf-8"))  # cut off a newline
#
#         Client.raw_send(self, sock, len(full_msg), full_msg)
#
#     def receive_msg_from(self, sock):
#         """This function waits for a message on a socket and returns the message type and text."""
#
#         header = Client.raw_receive(self, sock, Message.HEADER_LENGTH)
#         (msg_type, msg_length) = struct.unpack('!LL', header)
#
#         try:
#             msg_text = Client.raw_receive(self, sock, msg_length).decode("utf-8")
#             return msg_type, msg_text
#
#         except MemoryError as err:
#             print("MemoryError: " + err.message)
#             return None
#
#     def print_message(self, msg_type, msg_text):
#         """This function prints a message with the text length in a nice format."""
#
#         print((next(iter({k for k, v in Message.TYPES.items() if v == msg_type}))), len(msg_text), msg_text)
#
#     def send_static_msg(self, msg_type, msg_text, sock):
#         """This function sends a message to a socket."""
#
#         full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(
#             msg_text.strip().encode("utf-8"))  # cut off a newline
#
#         Client.raw_send(self, sock, len(full_msg), full_msg)


print(len("The quick brown fox jumps over the lazy dog!"))
print(len("And thats the way the cookie crumbles"))
print(len("XD"))
print(len("More is more!"))
print(len("Shake it off"))
print(len("Cry havoc and let slip the dogs of war"))
print(len("""O, pardon me, thou bleeding piece of earth,
That I am meek and gentle with these butchers!
Thou art the ruins of the noblest man
That ever lived in the tide of times.
Woe to the hand that shed this costly blood!
Over thy wounds now do I prophesy,--
Which, like dumb mouths, do ope their ruby lips,
To beg the voice and utterance of my tongue--
A curse shall light upon the limbs of men;
Domestic fury and fierce civil strife
Shall cumber all the parts of Italy;
Blood and destruction shall be so in use
And dreadful objects so familiar
That mothers shall but smile when they behold
Their infants quarter'd with the hands of war;
All pity choked with custom of fell deeds:
And Caesar's spirit, ranging for revenge,
With Ate by his side come hot from hell,
Shall in these confines with a monarch's voice
Cry 'Havoc,' and let slip the dogs of war;
That this foul deed shall smell above the earth
With carrion men, groaning for burial."""))

print(len("""Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""))
