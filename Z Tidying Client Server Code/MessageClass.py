
#import struct
#from ClientClass import *

class Message:

    TYPES = ["NORMAL",          #0
             "JOIN",            #1
             "USER",            #2
             "PASS",            #3
             "DIRECT",          #4
             "COMMAND",         #5
             "SERVER"]          #6

    HEADER_LENGTH = 8

    def __init__(self):
        pass


    def send_msg(self, msg_type, msg_text, sock):
        """This function sends a message to a socket."""

        print("sending ", msg_text)
        full_msg = struct.pack('!LL', msg_type, len(msg_text)) + bytes(msg_text.strip().encode("utf-8"))  # cut off a newline

        Client.raw_send(self, sock, len(full_msg), full_msg)


    def receive_msg_from(self, sock):
        """This function waits for a message on a socket and returns the message type and text."""

        header = Client.raw_receive(self, sock, Client.HEADER_LENGTH)
        (msg_type, msg_length) = struct.unpack('!LL', header)

        try:
            msg_text = Client.raw_receive(self, sock, msg_length).decode("utf-8")
            return msg_type, msg_text

        except MemoryError as err:
            print("MemoryError: " + err.message)
            return None


    def print_message(self, msg_type, msg_text):
        """This function prints a message with the text length in a nice format."""

        print("%s : %d : %s" % (Client.TYPES[msg_type], len(msg_text), msg_text))



