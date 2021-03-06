"""**********************************************************
  Grant Draper SFC5 - Chat Server (Server - DatabaseClass)
                    Chatterbox
                Script Pre-Requisites

                Python 3.6 Interpreter
                Modules: pypyodbc 1.3.4
**********************************************************"""

import pypyodbc

class Database:
    """Class called "Database", this contains a list of functions that can be
        executed to manipulate, or retrieve data from the database"""

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

        """This function creates a new user taking the user details and constructing an SQL
            string to execute. The sql string uses the SCOPE_IDENTITY() sql function, this
            uses the last primary key value, which is automatically created by the database
            when adding a new record.

            Basically allows the entering of 2 records in separate entity's, using the primary
            key of the first created record, as a foreign key in the other."""

        sqlcode = "insert into dbo.Users (FirstName, LastName, ScreenName) " \
                  "values ('{0}', '{1}', '{2}') " \
                  "insert into dbo.Passwords([HashedPassword], [CurrentPassword], [User_ID]) " \
                  "values ('{3}', 1, SCOPE_IDENTITY())".format(fname, lname, sname, pass_hash)
        Database.execute_sqlcode(self, sqlcode)
        return

    def create_new_chatroom(self, room_name, description, room_type):

        """This function allows the creation of a new chatroom record, it constructs an sql
            string to execute, adding in the room values."""

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

        """This function allows you to convert a screenname into a user_id."""

        sqlcode = "select User_ID from Users where ScreenName = '{0}'".format(uname)
        user_id = Database.fetch_data(self, sqlcode)

        if user_id:
            return user_id[0][0]
        else:
            return user_id


    def retrieve_room_id_from_room_name(self, room_name):

        """This function allows you to convert a room_name into a room_id."""

        sqlcode = "select Room_ID from ChatRooms where RoomName = '{0}'".format(room_name)
        room_id = Database.fetch_data(self, sqlcode)

        if room_id:
            return room_id[0][0]
        else:
            return room_id

    def add_user_to_chatroom(self, uname, room_name):

        """This function allows you to add a user to a room by specifying, who and where."""

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        if room_id:
            sqlcode = "insert into dbo.ChatRooms_Users (Room_ID, User_ID) " \
                      "values ('{0}', '{1}')".format(room_id, user_id)
            Database.execute_sqlcode(self, sqlcode)
            return True, "User added to Chatroom."
        else:
            return False, "Chatroom does not exist."

    def is_user_in_a_chatroom(self, uname):

        """This function allows you to check just by the username if the user is in a room,
            and if they are it will return the room they are in."""

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        sqlcode = "select Room_ID from Chatrooms_Users where User_id = '{0}'".format(user_id)
        room_id = Database.fetch_data(self, sqlcode)

        if room_id:
            return True, room_id
        else:
            return False, "False"

    def user_in_chatroom(self, uname, room_name):

        """This function will allow you to check if a user is in a specific room by specifying
            who and where."""

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        sqlcode = "select Room_User_ID from Chatrooms_Users " \
                  "where User_id = '{0}' and Room_ID = '{1}'".format(user_id, room_id)
        room_user_id = Database.fetch_data(self, sqlcode)

        if room_user_id:
            return True, room_user_id
        else:
            return False, "False"



    def remove_user_from_chatroom(self, uname, room_name):

        """This function allows you to remove a user from a specific chatroom, firstly
            the function will check to ensure that the client is still in the room.
            Then it will remove them by specifying who and where."""

        user_id = Database.retrieve_user_id_from_uname(self, uname)
        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        sqlcode = "select Room_User_ID from Chatrooms_Users " \
                  "where User_id = '{0}' and Room_ID = '{1}'".format(user_id, room_id)
        chatroom_user_id = Database.fetch_data(self, sqlcode)

        if chatroom_user_id:
            sqlcode = "delete from Chatrooms_Users where Room_User_ID = '{0}'".format(chatroom_user_id[0][0])
            Database.execute_sqlcode(self, sqlcode)
            return True, "User removed from Chatroom."
        else:
            return False, "Unable to remove user, user not in Chatroom."

    def write_to_logs_db(self, timestamp, uname, msg_type, msg_text, socket):

        """This function allows you to write to the server logs database table."""

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

    def view_all_chatrooms(self):

        """This function allows you to select all available public chatrooms."""

        sqlcode = "select RoomName from ChatRooms" \
                  " where RoomType_ID = '2' "

        available_rooms = Database.fetch_data(self, sqlcode)
        return available_rooms

    def create_private_chat(self, uname):

        """This function allows the creation of a new chatroom private record, it constructs an sql
        string to execute, adding in the room values."""

        room_name = "PRIVATE_ROOM-{0}".format(uname)
        description = "Private Chatroom - Max 2 members."
        room_type = 1
        sqlcode = "insert into dbo.ChatRooms (RoomName, Description, RoomType_ID) " \
                  "values ('{0}', '{1}', '{2}')".format(
                    room_name, description, room_type)

        Database.execute_sqlcode(self, sqlcode)
        return


    def count_users_in_private_room(self, room_name):

        """This function allows you to count the users in a private room by specifying the room name."""

        room_id = Database.retrieve_room_id_from_room_name(self, room_name)
        sqlcode = "select User_ID from Chatrooms_Users where Room_ID = '{0}'".format(room_id)
        count = Database.fetch_data(self, sqlcode)
        return len(count)

    def count_users_in_room(self, room_name):

        """This function allows you to count the users in a room by specifying the room name."""

        room_id = Database.retrieve_room_id_from_room_name(self, room_name)
        sqlcode = "select User_ID from Chatrooms_Users where Room_ID = '{0}'".format(room_id)
        count = Database.fetch_data(self, sqlcode)
        return len(count)

    def count_all_users(self):

        """This function allows you to count all registered users."""

        sqlcode = "select User_ID from Users"
        count = Database.fetch_data(self, sqlcode)
        print(type(count))
        return len(count)

    def count_all_chatrooms(self):

        """This function allows you to count all live chatrooms."""

        sqlcode = "select Room_ID from Chatrooms"
        count = Database.fetch_data(self, sqlcode)
        return len(count)


    def join_private_chatroom(self, uname, room_name):

        """This function allows you to join a private chatroom, as long as the room is not full."""

        room_id = Database.retrieve_room_id_from_room_name(self, room_name)

        if room_id:
            if Database.count_users_in_private_room(self, room_name) <= 1:
                Database.add_user_to_chatroom(self, uname, room_name)
                return True, "{0} has joined the room.".format(uname)
            else:
                return False, "Room Full"
        else:
            return False, "No Private Room Exists."

    def delete_chatroom(self, room_name):

        """This function allows you to delete a chatroom by its name."""

        sqlcode = "delete from Chatrooms where Room_ID = '{0}'".format(room_name)
        Database.execute_sqlcode(self, sqlcode)
        return

    def is_user_admin(self, uname):

        """This function allows you to check if a user has admin rights."""

        sqlcode = "select User_ID from dbo.Users where ScreenName = '{0}' and AdminRights = '1'".format(uname)
        check = Database.fetch_data(self, sqlcode)
        if check:
            return True
        else:
            return False

    def how_many_users_in_room(self, uname):

        """This function allows you to count users in a room, by screenname rather than room name"""

        room_id = Database.is_user_in_a_chatroom(self, uname)[1][0][0]
        sqlcode = "select count(User_ID) from ChatRooms_Users where Room_ID = '{0}'".format(room_id)
        check = Database.fetch_data(self, sqlcode)

        if check:
            return check[0][0]
        else:
            return False

    def does_chatroom_exist(self, room_name):

        """This function allows you to check if a chatroom is already present in th database."""

        sqlcode = "select Room_ID from ChatRooms where RoomName = '{0}'".format(room_name)
        check = Database.fetch_data(self, sqlcode)

        if check:
            return True
        else:
            return False