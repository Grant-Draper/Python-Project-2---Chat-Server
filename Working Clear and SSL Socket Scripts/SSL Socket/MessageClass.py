import struct

# Message format is:
#   4 bytes unsigned type
#   4 bytes unsigned length
#   Message data

TYPES = ["NORMAL"]
HEADER_LENGTH = 8



""" This is incomplete, need to finalise making this into a class"""


class Message:


    def send_msg(msg_type, msg_text, sock):
        """This function sends a message to a socket."""

        # original
        #full_msg = struct.pack('!LL', msg_type, len(msg_text) - 1) + msg_text.strip  # cut off a newline

        full_msg = struct.pack('!LL', msg_type, len(msg_text) - 1) + bytes(msg_text.strip().encode("utf-8"))  # cut off a newline     msg_text[:-1]

        Message.raw_send(sock, len(full_msg), full_msg)


    def receive_msg_from(sock):
        """This function waits for a message on a socket and returns the message type and text."""

        header = Message.raw_receive(sock, HEADER_LENGTH)
        (msg_type, msg_length) = struct.unpack('!LL', header)

        try:
            # oringinal
            #msg_text = Message.raw_receive(sock, msg_length)

            # working
            msg_text = Message.raw_receive(sock, msg_length).decode("utf-8")

            #msg_text = Message.raw_receive(sock.decode("utf-8"), msg_length)


            return msg_type, msg_text

        except MemoryError as err:
            print("MemoryError: " + err.message)
            return None


    def print_message(msg_type, msg_text):
        """This function prints a message with the text length in a nice format."""

        print("%s : %d : %s" % (TYPES[msg_type], len(msg_text), msg_text))


    def raw_receive(sock, length):
        """This function receives length bytes of raw data from a socket, returning the data."""

        chunks = []
        bytes_rx = 0

        while bytes_rx < length:
            chunk = sock.recv(length - bytes_rx)
            if chunk == b'':
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_rx += len(chunk)
        return b''.join(chunks)


    def raw_send(sock, length, data):
        """ This function sends raw data on a socket."""

        total_sent = 0

        while total_sent < length:
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket send failure")
            total_sent = total_sent + sent
