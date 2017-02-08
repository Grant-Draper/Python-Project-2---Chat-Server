# create a person
class Client:

    # to create a person yo need these values
    def __init__(self, first_name, last_name, user_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password


    # to describe a person
    def describe(client):
        print(client.first_name)
        print(client.last_name)
        print(client.user_name)
        print(client.password)

        for item in Client.__dict__:
            print(item)
        #print(Client.__dict__)

class chatRoom:

    def __init__(self, room_name):
        self.room_name = room_name


    def describe(chat_room):
        print(chat_room.room_name)

    def join(chat_room):
        print(chat_room.members)




       self.members = username



#c = Client("grant", "draper", "gdawg", "pass")
#c.describe()

