import pypyodbc


def opensqladminconnection(action, location, columns, values):

    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
    cursor = connection.cursor()
    #sqlcode = action + location + " ({0})".format(*columns) + " VALUES ({0})".format(*values)
    cursor.execute(sqlcode)
    connection.commit()
    cursor.close()
    connection.close()


    return

action = "INSERT INTO "
location = "Actions"
columns = ["Action, Description"]
values = ["'Logged out', 'User has been logged out from the system'"]


OpenServerAdminConnection(action, location, columns, values)
#


class Database:

    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;"
                                  "Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
    cursor = connection.cursor()

    #def connect_to_database(self):

    def execute_sqlcode(self, sqlcode):

        #cursor = Database.connection.cursor()
        cursor.execute(sqlcode)
        Database.connection.commit()

    def disconnect_from_database(self):
        Database.cursor.cursor.close()
        Database.connection.close()

    def database_add_line_to_table(self, table, columns, values):
        action = "INSERT INTO "

        self.database_table = table
        self.database_columns = columns
        self.database_values = values

        sqlcode = action + table + " ({0})".format(*columns) + " VALUES ({0})".format(*values)

        Database.execute_sqlcode(sqlcode)












# create a person
class Client:

    clients = {"first_name": str(), "last_name": str(), "user_name": None,
               "password": None, "logged_in": None, "logged_out": None}

    # to create a person you need these values
    def __init__(self, first_name, last_name, user_name, password):


        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password

        Client.clients.update({"first_name": first_name, "last_name": last_name, "user_name": user_name, "password": password})



    # to describe a person
    def describe(client):
        print(client.first_name)
        print(client.last_name)
        print(client.user_name)
        #print(client.password)

        # for item in Client.__dict__:
        #     print(item)
        #print(Client.__dict__)


c1 = Client("grant", "draper", "gdawg", "pass")
c2 = Client("robert", "geldof", "boby", "pass")

c1.describe()
c2.describe()

print(clients)






# class ChatRoom:
#
#     def __init__(self, room_name):
#         self.room_name = room_name
#
#     def describe(chat_room):
#         print(chat_room.room_name)
#
#     def join(chat_room):
#         print(chat_room.members)
#
#
#
# class Message:
#
#     def __init__(self, type, text_length, text):
#         self.type =
#
#
#
#
#
# class MessageType(Message):
#
#     message_type = {
#                     1 = "NORMAL"
#                     2 = "JOIN"
#                     3 = "USER"
#                     4 = "PASS"
#                     5 = "DIRECT"
#                     6 = "COMMAND"
#                     7 = "SERVER"
#                     }
#
#
#
#
#     def __init__(self):
#         self.message_type =
#

