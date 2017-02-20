import pypyodbc
import pprint


class Database:

    """Class called "Database", this contains a list of functions that can be
        executed to manipulate of retrieve data from the database"""

    sql_commands = [
        " SELECT ", " FROM ", " WHERE ", " AND ", " OR ",
        " INSERT INTO ", " VALUES ", " UPDATE ", " SET ",
        " DELETE ", " TOP "
    ]

    # connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;"
    #                               "Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;"
                                  "Database=Test;""uid=DatabaseAdmin;pwd=Password01")
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
            sqlcode = action[0] + " {0} ".format(retrive_columns) + action[1] + table + action[2] + " {0} ".format(comparison_column) + action[3].format(clause)
            return Database.fetch_data(self, sqlcode)
        else:
            sqlcode = action[0] + " {0} ".format(*retrive_columns) + action[1] + table + action[2] + " {0} ".format(comparison_column) + action[3].format(clause)
            return Database.fetch_data(self, sqlcode)



d = Database()

#d.add_line_to_table("MessageType", "MessageType", "'LEAVE'")
# d.add_line_to_table("Actions", ["Action, Description"], ["'Test', 'This is test input 3'"])
# d.add_line_to_table("Actions", ["Action, Description"], ["'Test', 'This is test input 4'"])

#print(d.select_from_table(["Action, Description"], "Actions"))
#print(d.select_from_table("MessageType", "MessageType"))
#pprint.pprint(d.select_from_table("*", "MessageType"))

#print(d.select_from_table("ScreenName", "Users"))

print(d.select_from_table_where("ScreenName", "Users", "User_ID", "1"))
print(d.select_from_table_where(["FirstName, LastName, ScreenName"], "Users", "User_ID", "1"))