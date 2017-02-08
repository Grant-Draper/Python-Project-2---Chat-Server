def select_from_table(columns, table):
    """"""

    action = ["SELECT ", "FROM "]

    sqlcode = action[0] + " {0} ".format(*columns) + action[1] + table

    print(sqlcode)

    pass



select_from_table(["Action, Description"], "Actions")