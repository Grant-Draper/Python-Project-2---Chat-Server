import pypyodbc


class Database:

    """Class called "Database", this contains a list of functions that can be
        executed to manipulate of retrieve data from the database"""

    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;"
                                  "Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
    cursor = connection.cursor()



    def execute_sqlcode(self, sqlcode):

        """Function called "execute_sqlcode" to take the single argument "sqlcode" from
            another function and apply that to the database committing changes."""

        Database.cursor.execute(sqlcode)
        Database.connection.commit()



    def disconnect(self):

        """Function called "disconnect" which closes the database connection gracefully."""

        Database.cursor.close()
        Database.connection.close()



    def add_line_to_table(self, table, columns, values):

        """Function called "add_line_to_table" which takes the arguments "table", columns"
            and "values" and constructs the variable "sqlcode". This variable is then
            passed to the "execute_sqlcode" function."""

        action = "INSERT INTO "

        # self.database_table = table
        # self.database_columns = columns
        # self.database_values = values

        sqlcode = action + table + " ({0})".format(*columns) + " VALUES ({0})".format(*values)

        Database.execute_sqlcode(self, sqlcode)



    def remove_line_from_table(self):
        pass



    def modify_line_in_table(self):
        pass



    def select_from_table(self, columns, table):

        """"""

        action = ["SELECT ", "FROM "]

        sqlcode = action[0] + " {0} ".format(*columns) + action[1] + table

        return Database.execute_sqlcode(self, sqlcode)









d = Database()

# d.add_line_to_table("Actions", ["Action, Description"], ["'Test', 'This is test input 3'"])
# d.add_line_to_table("Actions", ["Action, Description"], ["'Test', 'This is test input 4'"])

print(d.select_from_table(["Action, Description"], "Actions"))