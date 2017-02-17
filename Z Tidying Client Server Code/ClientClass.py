#import struct
#import socket

# Message format is:
#   4 bytes unsigned type
#   4 bytes unsigned length
#   Message data

#TYPES = ["NORMAL"]
#HEADER_LENGTH = 8


class Client:


    def __init__(self, HOST, PORT):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_socket = ssl.wrap_socket(server_socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
            ssl_socket.connect((HOST, PORT))

        except Exception as e:
            print(e)
            print("Completed with Exception1.", "\n")
            pass


    def listening(self):

        while True:

            # 6. check if input has been received from stdin or the server_socket
            available_streams, _, _ = select.select([sys.stdin, ssl_socket], [], [], 1)

            # 7. if sys.stdin is available to read, read from it and send the message
            if sys.stdin in available_streams:
                msg_text = sys.stdin.readline()
                Message.send_msg(Message.TYPES[0], msg_text, ssl_socket)
            continue

            # 8. if the server socket is available to read, read from it and print the message
            if ssl_socket in available_streams:
                msg_type, msg_text = Message.receive_msg_from(ssl_socket)
                print(msg_type, msg_text)
            continue


    def raw_receive(self, sock, length):
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


    def raw_send(self, sock, length, data):
        """ This function sends raw data on a socket."""

        total_sent = 0

        while total_sent < length:
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket send failure")
            total_sent = total_sent + sent
