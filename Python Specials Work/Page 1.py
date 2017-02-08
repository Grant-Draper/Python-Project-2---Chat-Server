import time


course = []

delegate = {
        "firstname": None,
        "lastname": None,
        "username": None,
        "password": None,
        "logged_in": None,
        "logged_out": None
        }



def log_in(username, password):

    if username == delegate["username"] and password == delegate["password"]:

        course.append(delegate["firstname" + "lastname"])
        delegate["logged_in"].append(time.ctime())
        return "Log in successful"

    else:

        return "Username or password incorrect, please try again"



def log_out(username, password):

    if username == delegate["username"] and password == delegate["password"]:

        course.remove(delegate["firstname" + "lastname"])
        delegate["logged_out"].append(time.ctime())
        return "Log out successful"

    else:
        return "Username or password incorrect, unable to log out."



def create_new_delegate(firstname, lastname, username, password):

    delegate[firstname, lastname, username, password].update(firstname, lastname, username, password)

    return "New user added"


#
# #### Testing loop
#
# def testing_loop():
#
#     while True:
#
#





create_new_delegate(input("Please enter your firstname: "),
                    input("Please enter your lastname: "),
                    input("Please enter a username: "),
                    input("Please enter a password: "))

log_in(input("Please enter a username."),
       input("Please enter a password"))

print(delegate)
