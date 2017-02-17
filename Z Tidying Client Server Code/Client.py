
"""**********************************************************
        Grant Draper SFC5 - Chat Server (Client)
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules: pypyodbc 1.3.4
**********************************************************"""

import select
import socket
import ssl
import sys

from MessageClass import *
from ClientClass import *

#Host = "192.168.1.201"
# Host = "127.0.0.1"
# Port = 30000
# NORMAL = 0


c1 = Client("192.168.1.201", 30000)

c1.listening()



















