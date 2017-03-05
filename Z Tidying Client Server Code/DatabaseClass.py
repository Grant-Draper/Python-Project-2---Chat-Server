import pypyodbc
import pprint


class Database:

    """Class called "Database", this contains a list of functions that can be
        executed to manipulate of retrieve data from the database"""

    sql_commands = [
        " SELECT ",  # 0
        " FROM ",  # 1
        " WHERE ",  # 2
        " AND ",  # 3
        " OR ",  # 4
        " INSERT INTO ",  # 5
        " VALUES ",  # 6
        " UPDATE ",  # 7
        " SET ",  # 8
        " DELETE ",  # 9
        " TOP ",  # 10
        " = '{0}' "  # 11
    ]

    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;"
                                   "Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
    #connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;"
    #                              "Database=Test4;""uid=DatabaseAdmin;pwd=Password01")
    cursor = connection.cursor()

    def execute_sqlcode(self, sqlcode):

        """Function called "execute_sqlcode" to take the single argument "sqlcode" from
            another function and apply that to the database committing changes."""

        Database.cursor.execute(sqlcode)
        Database.connection.commit()

    def fetch_data(self, sqlcode):

        """Function called "fetch_data" to take the single argument "sqlcode" from
            another function and "fetchall" matching the query from the database."""

        Database.cursor.execute(sqlcode)

        return Database.cursor.fetchall()

    def disconnect(self):

        """Function called "disconnect" which closes the database connection gracefully."""

        Database.cursor.close()
        Database.connection.close()

    def add_line_to_table(self, table, columns, values):

        """Function called "add_line_to_table" which takes the arguments "table", columns"
            and "values" and constructs the variable "sqlcode". This variable is then
            passed to the "execute_sqlcode" function.

            table - Where you want to affect data (The Entity/Table Name)
            columns - The columns you want to affect within the location
            values - The information you want to insert into the database

            ***IMPORTANT: All "Values" must use single quotes within the python string
            composer, this indicates to SQL that the values are strings!!
            e.g. "'Logged Out', 'User has been logged out'" """

        action = Database.sql_commands[5]

        if type(columns) != list:

            sqlcode = action + table + " ({0})".format(columns) + " VALUES ({0})".format(values)
            Database.execute_sqlcode(self, sqlcode)
        else:
            sqlcode = action + table + " ({0})".format(*columns) + " VALUES ({0})".format(*values)
            Database.execute_sqlcode(self, sqlcode)

    def remove_line_from_table(self):
        pass

    def modify_line_in_table(self):
        pass

    def select_from_table(self, columns, table):

        """Function called "select_from_table", takes the arguments "columns" and
            "table" and constructs the variable "sqlcode". This variable is then
            passed to the "execute_sqlcode" function.

            table - Where you want to select data (The Entity/Table Name)
            columns - The columns you want to find within the table, or
                        use * to select ALL columns. """

        if type(columns) != list:

            sqlcode = Database.sql_commands[0] + " {0} ".format(columns) + Database.sql_commands[1] + table
            return Database.fetch_data(self, sqlcode)
        else:
            sqlcode = Database.sql_commands[0] + " {0} ".format(*columns) + Database.sql_commands[1] + table
            return Database.fetch_data(self, sqlcode)

    def select_from_table_where(self, retrive_columns, table, comparison_column, clause):

        """Function called "select_from_table_where", takes the arguments:
            retrieve_columns = what you wan to return if the pattern is matched
            table = where you want to look
            comparison_column = what information do you want to compare with te clause
            clause = the information you would like to compare. """

        action = ["SELECT ", "FROM ", " WHERE ", " = '{0}' "]

        if type(retrive_columns) != list:
            sqlcode = action[0] + " {0} ".format(retrive_columns) + action[1] + table + action[2] + " {0} ".format(
                comparison_column) + action[3].format(clause)
            return Database.fetch_data(self, sqlcode)
        else:
            sqlcode = action[0] + " {0} ".format(*retrive_columns) + action[1] + table + action[2] + " {0} ".format(
                comparison_column) + action[3].format(clause)
            return Database.fetch_data(self, sqlcode)


    def select_screenname_if_passhash_matches(self, pswd):

        """Function with a single argument, designed to check a hashed password value
            against the passwords in the database, that are linked to a user account.
            the function will check 2 things, the password exists and it is marked as
             the current password. if the value is matched, the function will return the
             screenname of the user it is linked to. this can then be compared to the
             screenname provided by the user."""

        sqlcode = "select ScreenName from Users " \
                  "inner join Passwords on Users.User_ID=Passwords.User_ID " \
                  "where Passwords.HashedPassword='{0}' and Passwords.CurrentPassword=1".format(pswd)

        user = Database.fetch_data(self, sqlcode)

        return user


    def create_new_user(self, fname, lname, sname, pass_hash):

        """"""

        sqlcode = "insert into dbo.Users (FirstName, LastName, ScreenName) " \
                  "values ('{0}', '{1}', '{2}') " \
                  "insert into dbo.Passwords([HashedPassword], [CurrentPassword], [User_ID]) " \
                  "values ('{3}', 1, SCOPE_IDENTITY())".format(fname, lname, sname, pass_hash)
        Database.execute_sqlcode(self, sqlcode)

        return

    def create_new_chatroom(self, room_name, description, room_type):

        """"""

        if room_type == "Private":
            room_type = 1
        elif room_type == "Public":
            room_type = 2

        sqlcode = "insert into dbo.ChatRooms (RoomName, Description, RoomType_ID) " \
                  "values ('{0}', '{1}', '{2}')".format(
            room_name, description, room_type)

        Database.execute_sqlcode(self, sqlcode)
        return

    def retrieve_user_id_from_uname(self, uname):

        sqlcode = "select User_ID from Users where ScreenName = '{0}'".format(uname)
        user_id = Database.fetch_data(self, sqlcode)
        return user_id[0][0]

    def retrieve_room_id_from_room_name(self, room_name):

        sqlcode = "select Room_ID from ChatRooms where RoomName = '{0}'".format(room_name)
        room_id = Database.fetch_data(self, sqlcode)
        return room_id[0][0]

    def add_user_to_chatroom(self, uname, room_name):

        """"""

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        if bool(room_id) is False:
            print("Chatroom does not exist.")
            return False, "Chatroom does not exist."

        else:
            sqlcode = "insert into dbo.ChatRooms_Users (Room_ID, User_ID) " \
                      "values ('{0}', '{1}')".format(room_id, user_id)
            Database.execute_sqlcode(self, sqlcode)
            return True, "User added to Chatroom."
    """
    def is_user_in_chatroom(self, uname, room_name):

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        sqlcode = "select Room_User_ID from Chatrooms_Users where User_id = '{0}' and Room_ID = '{1}'".format(user_id, room_id)
        room_user_id = Database.fetch_data(self, sqlcode)

        if room_user_id:
            return True
        else:
            return False
    """
    def is_user_in_chatroom(self, uname):

        user_id = Database.retrieve_user_id_from_uname(self, uname)

        sqlcode = "select Room_ID from Chatrooms_Users where User_id = '{0}'".format(user_id)
        room_id = Database.fetch_data(self, sqlcode)

        if room_id:
            return True, room_id
        else:
            return False, "False"


    def remove_user_from_chatroom(self, uname, room_name):

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        sqlcode = "select Room_User_ID from Chatrooms_Users " \
                  "where User_id = '{0}' and Room_ID = '{1}'".format(user_id, room_id)
        chatroom_user_id = Database.fetch_data(self, sqlcode)[0][0]

        if bool(chatroom_user_id):
            sqlcode = "delete from Chatrooms_Users where Room_User_ID = '{0}'".format(chatroom_user_id)
            Database.execute_sqlcode(self, sqlcode)
            print("True")
            return True, "User removed from Chatroom."

        else:
            print("False")
            return False, "Unable to remove user, user not in Chatroom."

    def write_to_logs_db(self, timestamp, uname, msg_type, msg_text, socket):

        """"""

        if uname == "Unknown Client":
            user_id = 0
        else:
            user_id = Database.retrieve_user_id_from_uname(self, uname)

        socket = str(socket)
        socket = socket.replace("'", "")

        sqlcode1 = "insert into logs (DateTime, User_ID, MessageType, Message, Socket) " \
                   "values ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
                    timestamp, user_id, msg_type, msg_text, socket)

        Database.execute_sqlcode(self, sqlcode1)
        return

"""
value = "value2"
dict = {"key":"value", "key2":"value2", "key3":"value3"}

print((next(iter({k for k, v in dict.items() if v == value}))))
"""




#d = Database()
"""
d = Database()
if d.is_user_in_chatroom("gd", "loosygoosy"):
    print(1)
else:
    print(2)
"""
#d.add_user_to_chatroom("gdawg", "loosygoosy")

# Database.create_new_user(db, grant, draper, gdawg, siofvsndfcvlsknc)


#d.create_new_chatroom("thisisroomy", "quite spacious", "Public")


#print(d.select_screenname_if_passhash_matches("nofear"))

# d.add_line_to_table("MessageType", "MessageType", "'LEAVE'")
# d.add_line_to_table("Actions", ["Action, Description"], ["'Test', 'This is test input 3'"])
# d.add_line_to_table("Actions", ["Action, Description"], ["'Test', 'This is test input 4'"])

# print(d.select_from_table(["Action, Description"], "Actions"))
# print(d.select_from_table("MessageType", "MessageType"))
# pprint.pprint(d.select_from_table("*", "MessageType"))

# print(d.select_from_table("ScreenName", "Users"))

#print(d.select_from_table_where("ScreenName", "Users", "User_ID", "98459"))
#print(d.select_from_table_where(["FirstName, LastName, ScreenName"], "Users", "User_ID", "1"))