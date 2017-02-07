import pypyodbc


## WORKING function adaptable to different ammounts of columns etc
## using string substitution with .format function.

def opensqladminconnection(action, location, columns, values):

    """Function called opensqladminconnection, which takes 4 arguments.

        action - What SQL function you would like to apply
        location - Where you want to affect data (The Entity/Table Name)
        columns - The columns you want to affect within the location
        values - The information you want to find or insert into the database

        ***IMPORTANT: All "Values" must use single quotes within the python string composer, this indicates
            to SQL that the values are strings!!
            e.g. "'Logged Out', 'User has been logged out'" """

    # Connection string to connect to the database with Admin creds.
    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")

    # Connection cursor assignment.
    cursor = connection.cursor()

    # SQL code string composer identifier.
    sqlcode = action + location + " ({0})".format(*columns) + " VALUES ({0})".format(*values)

    # Actions the SQL code.
    cursor.execute(sqlcode)

    # Commits changes to database, closes cursor and connection.
    connection.commit()
    cursor.close()
    connection.close()


    return

action = "INSERT INTO "
location = "Actions"
columns = ["Action, Description"]
values = ["'Logged out', 'User has been logged out from the system'"]


OpenServerAdminConnection(action, location, columns, values)







# ### WORKING function that opens connection to server and inputs data to a table (FIXED VALUES!)


# def OpenServerAdminConnection():
##
#     connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
#
#     cursor = connection.cursor()
#     SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")

#     Values = ["Log in unsuccessful", "Either username or password is incorrect"]
#
#     cursor.execute(SQLCommand, Values)
#
#     connection.commit()
#     connection.close()
#
#
#     return
#
# OpenServerAdminConnection()

