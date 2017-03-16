
"""**********************************************************
        Grant Draper SFC5 - Chat Server (Server)
                    Chatterbox
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules: pypyodbc 1.3.4
**********************************************************"""

from ServerClass import *

a = Server("192.168.1.201", 30000)
#b = Server("192.168.1.201", 30001)


a.listening()
#b.listening()









