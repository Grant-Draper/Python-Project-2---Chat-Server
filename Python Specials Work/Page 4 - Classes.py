members = []

delegates = {"first_name": str(), "last_name": str()}


class Room:

    def __init__(self, name, delagates):
        self.name = name
        self.delegates = []




    def room_accept_delegate(self, delegate):
        self.delegates.append(delegate)






    # def leave_room(self, leave_room):
    #     self.leave_room = leave_room
    #     members -= self
    #     pass




class Delegate:

    def __init__(self, name, cohort):
        self.name = name
        self.cohort = cohort



    def create_new(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

        delagates.update(self)

    def __str__(self):
        return self.name

        pass

    def update_delegate(self):
        pass

    def delete_delegate(self):
        pass


    pass


u1 = Delegate.create_new("grant", "draper")