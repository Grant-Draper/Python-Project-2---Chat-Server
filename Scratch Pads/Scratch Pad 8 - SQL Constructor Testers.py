
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

def insert_into_table(table, columns, values):

    action = "INSERT INTO "

    if type(columns) != list:

        sqlcode = action + table + " ({0})".format(columns) + " VALUES ({0})".format(values)
    else:
        sqlcode = action + table + " ({0})".format(*columns) + " VALUES ({0})".format(*values)

    print(sqlcode)

    pass

insert_into_table("MessageType", "MessageType", "'JOIN'")
insert_into_table("Actions", ["Action, Description"], ["'Test', 'This is test input 4'"])





















