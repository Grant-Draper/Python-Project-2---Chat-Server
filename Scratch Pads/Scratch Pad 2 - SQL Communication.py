import pypyodbc

#
#
# ## trying to change the code to use print substitution
#
# def OpenServerAdminConnection(Action, Location, Columns, Values):
#
#
#     connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
#
#     cursor = connection.cursor()
#
#     action = Action
#     location = Location
#     columns = Columns
#     values = Values
#
#
#     #SQLCommand = str("{0}{1}".format(action, location), "({0})".format(columns), "VALUES (?,?)") # "VALUES ({0})".format(values))
#
#     SQLCommand = ("%s, %s" % (action, location))
#
#     #SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")
#
#
#     print(repr(SQLCommand), 1)
#     print(type(SQLCommand), 1)
#
#     cursor.execute(SQLCommand, values) #, Values
#
#     print(repr(SQLCommand), 2)
#     print(type(SQLCommand), 2)
#
#     connection.commit()
#     connection.close()
#
#
#     return
#
# Action = "INSERT INTO "
# Location = "Actions"
# Columns = "Action,Description"
# Values = ["Logged out, User has been logged out from the system"]
#
#
# OpenServerAdminConnection(Action, Location, Columns, Values)









## Trying to reformat code to make the function adaptable to different ammounts of columns etc
## using string substitution with .format function. am going to try with just substitution

def OpenServerAdminConnection(Action, Location, Columns, Values):


    connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")

    cursor = connection.cursor()

    action = Action
    location = Location
    columns = Columns
    values = Values


    #SQLCommand = ("{0}{1}".format(action, location), "({0})".format(columns), "VALUES (?,?)") # "VALUES ({0})".format(values))
    #SQLCommand = ("{0}{1}".format(action, location), "({0})".format(columns), "VALUES ({0})".format(values))


    #SQLCommand = ("{0}{1}".format(action, location), "({0}{1})".format(columns), "VALUES ({0})".format(values))

    #SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")

    # print(repr(SQLCommand), 1)
    # print(type(SQLCommand), 1)

    # print(SQLCommand)
    # print(repr(SQLCommand))

    print("\n")

    #cursor.execute("{0}{1}".format(action, location), "({0})".format(columns), "VALUES ({0})".format(values)) #, Values
    #print(action, location, *columns, *values)
    #cursor.execute(*action, *location, *columns, *values)
    #cursor.execute(SQLCommand, Values)

    #cursor.execute(action, location, "({0})".format(*columns + ","), "VALUES ({0})".format(*values))
    #print(action, location, "({0})".format(*columns), "VALUES ({0})".format(*values))

    #sqlcode = (action, location, "({0})".format(*columns), "VALUES ({0})".format(*values))
    sqlcode = action + location + " ({0})".format(*columns) + " VALUES ({0})".format(*values)

    print(sqlcode)

    #cursor.execute(action, location, "({0})".format(*columns), "VALUES ({0})".format(*values))
    cursor.execute(sqlcode)

    # print(repr(SQLCommand), 2)
    # print(type(SQLCommand), 2)

    connection.commit()
    cursor.close()
    connection.close()


    return

Action = "INSERT INTO "
Location = "Actions"
Columns = ["Action, Description"]
Values = ["Logged out, User has been logged out from the system"]




# Values = ["Logged In OK", "User has successfully authenticated"]
#
# SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")


OpenServerAdminConnection(Action, Location, Columns, Values)







# ### Working code that opens connection to server and inputs data to a table
# def OpenServerAdminConnection():
#
#
#     connection = pypyodbc.connect("Driver={SQL Server};""Server=WIN-4LSB61AA7VI\SQLEXPRESSPYTHON;""Database=PythonProject2DB;""uid=DatabaseAdmin;pwd=Password01")
#
#     cursor = connection.cursor()
#     SQLCommand = ("INSERT INTO Actions""(Action,Description)""VALUES (?,?)")
#
#     print(repr(SQLCommand), 1)
#     print(type(SQLCommand), 1)
#
#     Values = ["Log in unsuccessful", "Either username or password is incorrect"]
#
#     cursor.execute(SQLCommand, Values)
#
#     print(repr(SQLCommand), 2)
#     print(type(SQLCommand), 2)
#
#     connection.commit()
#     connection.close()
#
#
#     return
#
# OpenServerAdminConnection()

