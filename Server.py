
"""**********************************************************
        Grant Draper SFC5 - Chat Server (Server)
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules:
**********************************************************"""

import socket, ssl, json, select, pprint
from datetime import datetime

"""starting to try and implement sockets"""


def FileScan(python_data):
    while True:
        while True:
            print("Filepath:", python_data[7])
            for s in (python_data[5]):
                print("Directory has", python_data[4], "files, which consume", s)
            # print("Total number of files:", python_data[4])
            print("Contents:")
            for i in (python_data[3]):
                print(i)
            print(" ")
            print(" ")
            break
        print("Directory Scanned:", python_data[2])
        print("Total Size of Directory:", python_data[6])
        print("\n", "----------------------------------------------------------------", "\n")

        break
    return



Host = ""
Port = 30000


master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
master_socket.setblocking(0)
master_socket.bind((Host, Port))
master_socket.listen(1)

sockets = []
sockets.append(master_socket)


def Listening():

    while True:
        (readable, writable, exceptional) = select.select(sockets, [], sockets)

        for s in readable:
            if s is master_socket:
                (client, _) = master_socket.accept()
                ssl_socket = ssl.wrap_socket(client, server_side=True, certfile="server.crt", keyfile="server.key")
                ssl_socket.setblocking(0)
                sockets.append(ssl_socket)
                # print("Open Server Connections")
                # print(sockets)

            else:
                incoming_data = ssl_socket.read()

                if not incoming_data:
                    ssl_socket.shutdown(socket.SHUT_RDWR)
                    ssl_socket.close()
                    sockets.remove(ssl_socket)
                else:
                    decoded_data = incoming_data.decode("UTF-8")
                    python_data = json.loads(decoded_data)
                    outgoing_data = "Server Received Data"
                    ssl_socket.write(outgoing_data.encode("UTF-8"))

                    # if python_data[0] == "TimeStamp":
                    #     print(python_data[0], "Function Information Received")
                    #     print("From host: ", python_data[1])
                    #     print(python_data[2], "\n ")

                    if python_data[0] == "PlatformInfo":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")

                        items = []
                        for i in python_data[2]:
                            items.append(i)

                        #print(items)
                        print("Device hostname:              ", items[1])
                        print("Operating system:             ", items[0])
                        print("Operating system release:     ", items[2])
                        print("Operating system version:     ", items[3])
                        print("Machine type:                 ", items[4])
                        print("Processor type:               ", items[5], "\n ")
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "Partitions":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")

                        items = []
                        for i in python_data[2]:
                            items.append(i)
                        print(items)
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "PartUsage":

                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")

                        for key in python_data[2]:
                            try:

                                value = python_data[2][key]

                                if value[0] == "exception":
                                    print(key)
                                    print(value[1], "\n")

                                else:
                                    print(key)
                                    print(value[0])
                                    print(value[1])
                                    print(value[2], "\n")

                            except Exception as e:
                                print(e)
                                pass
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "User":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")
                        print("Currently Active User:", "\n ")
                        print(python_data)
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "PSTable":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")
                        print(python_data)
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "NICs":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")
                        pprint.pprint(python_data)
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "NICAddr":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")
                        print(python_data)
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "Sockets":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")
                        print(python_data)
                        print("\n", "----------------------------------------------------------------", "\n")

                    elif python_data[0] == "FileScan":
                        print(python_data[0], "Function Information Received")
                        ts = datetime.now()
                        print("From host: ", python_data[1], "at", ts.hour, ":", ts.minute, "on", ts.day, "/", ts.month, "/", ts.year, "\n")
                        FileScan(python_data)
                        print("\n", "----------------------------------------------------------------", "\n")


                    else:
                        print("invalid")









Listening()










