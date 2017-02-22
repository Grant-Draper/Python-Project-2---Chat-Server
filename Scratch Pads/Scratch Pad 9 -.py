# sql_commands = [
#     " SELECT ", " FROM ", " WHERE ", " AND ", " OR ",
#     " INSERT INTO ", " VALUES ", " UPDATE ", " SET ",
#     " DELETE ", " TOP "
# ]
#
# print(repr(sql_commands[5]))
#
#
#


import struct
#
#
# NORMAL = 0
#
#
#
# def send_msg(msg_type, msg_text, sock):
#     """This function sends a message to a socket."""
#
#     full_msg = struct.pack('!LL', msg_type, len(msg_text) - 1) + msg_text.strip  # cut off a newline     msg_text[:-1]
#
#     raw_send(sock, len(full_msg), full_msg)
#
#
#
#
#
# send_msg(NORMAL, "this is a test", server_socket)

# msg_text = "7his157h33nd".encode("utf-8")
#
# msg_text = bytes(msg_text)
#
# print(msg_text)

#
# msg_text = "blah blah blah" \
#            "woop de woop" \
#            "loop de loop"
#
# print(len(msg_text))
# print(msg_text.strip())
# print(len(msg_text.strip()))
# print(bytes(msg_text.strip().encode("utf-8")))
#
#





# full_msg = struct.pack('!LL', 0, len(msg_text) - 1) + bytes(msg_text.strip().encode("utf-8"))  # cut off a newline     msg_text[:-1]
#
#
# byte = bytes("testy".encode("utf-8"))
#
#
# print(full_msg.decode("utf-8"))
#
# print(byte)
#
# print(byte.decode("utf-8"))




TYPES = {"NORMAL": 0,  # 0
         "JOIN": 1,  # 1
         "USER": 2,  # 2
         "PASS": 3,  # 3
         "DIRECT": 4,  # 4
         "COMMAND": 5,  # 5
         "SERVER": 6}  # 6

print((next(iter({v for k, v in TYPES.items() if k == "SERVER"}))))
print(v for k, v in TYPES.items() if k == "SERVER")





























