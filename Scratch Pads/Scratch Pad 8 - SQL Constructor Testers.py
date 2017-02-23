
## SELECT Tester
#
# def select_from_table(columns, table):
#
#     action = ["SELECT ", "FROM "]
#     sqlcode = action[0] + " {0} ".format(*columns) + action[1] + table
#
#     print(sqlcode)
#
#     pass
#
# select_from_table(["Action, Description"], "Actions")


#
# ## INSERT INTO Single Tester
#
# def insert_into_table(table, columns, values):
#
#     action = "INSERT INTO "
#     sqlcode = action + table + " ({0})".format(columns) + " VALUES ({0})".format(values)
#
#     print(sqlcode)
#
#     pass
#
# insert_into_table("MessageType", "MessageType", "'JOIN'")
#


# ## INSERT INTO Multiple Tester
#
# def insert_into_table(table, columns, values):
#
#     action = "INSERT INTO "
#     sqlcode = action + table + " ({0})".format(*columns) + " VALUES ({0})".format(*values)
#
#     print(sqlcode)
#
#     pass
#
# insert_into_table("Actions", ["Action, Description"], ["'Test', 'This is test input 4'"])
#



## INSERT INTO Single and Multiple Tester
#
# def insert_into_table(table, columns, values):
#
#     action = "INSERT INTO "
#
#     if type(columns) != list:
#
#         sqlcode = action + table + " ({0})".format(columns) + " VALUES ({0})".format(values)
#     else:
#         sqlcode = action + table + " ({0})".format(*columns) + " VALUES ({0})".format(*values)
#
#     print(sqlcode)
#
#     pass
#
# insert_into_table("MessageType", "MessageType", "'JOIN'")
# insert_into_table("Actions", ["Action, Description"], ["'Test', 'This is test input 4'"])
#


## SELECT FROM WHERE Tester

#def select_from_table_where(retrive_columns, table, comparison_column, clause):
#
#    action = ["SELECT ", "FROM ", " WHERE ", " = '{0}' "]
#    #print(type(retrive_columns))
#
#    if type(retrive_columns) != list:
#        sqlcode = action[0] + " {0} ".format(retrive_columns) + action[1] + table + action[2] + " {0} ".format(comparison_column) + action[3].format(clause)
#
#    else:
#        sqlcode = action[0] + " {0} ".format(*retrive_columns) + action[1] + table + action[2] + " {0} ".format(comparison_column) + action[3].format(clause)
#
#    print(sqlcode)
#
#    pass
#
#select_from_table_where("ScreenName", "Users", "User_ID", "1" )
#select_from_table_where(["FirstName, LastName, ScreenName"], "Users", "User_ID", "1")


def create_new_user(fname, lname, sname, pass_hash):

    """"""

    sqlcode = "insert into dbo.Users (FirstName, LastName, ScreenName) values ('{0}', '{1}', '{2}') insert into dbo.Passwords([HashedPassword], [CurrentPassword], [User_ID]) values ('{3}', 1, SCOPE_IDENTITY())".format(fname, lname, sname, pass_hash)
    print(sqlcode)




create_new_user("grant", "draper", "gdawg", "siofvsndfcvlsknc")














