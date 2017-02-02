import pypyodbc



def OpenServerAdminConnection(Action, Location, Columns, Values):


    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")

    cursor = connection.cursor()

    action = Action
    location = Location
    columns = Columns
    values = Values


    SQLCommand = ("{0}{1}".format(action, location)"({0}{1})".format(columns)"VALUES ({0})".format(values))



    cursor.execute(SQLCommand, Values)
    connection.commit()
    connection.close()


    return

Action = "INSERT INTO"
Location = "Actions"
Columns = "Action, Description"
Values = "Log in unsuccessful, Either username or password is incorrect"




# Values = ["Logged In OK", "User has successfully authenticated"]
#
# SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")


OpenServerAdminConnection(Action, Location, Columns, Values)







### Working code that opens connection to server and inputs data to a table
# def OpenServerAdminConnection():
#
#
#     connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
#
#     cursor = connection.cursor()
#     SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")
#
#     Values = ["Logged In OK", "User has successfully authenticated"]
#
#     cursor.execute(SQLCommand, Values)
#     connection.commit()
#     connection.close()
#
#
#     return
#
# OpenServerAdminConnection()

