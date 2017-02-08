class Dog:
    def __init__(self, name):
        self.name = name
        self.weight = None
        self.speaks ="woof!"


    def speaks(name, says):
        #name.speaks = says
        print(name.speaks)

    def eats(name, amount):
        name.weight = amount


class Cat:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.speaks = "purr!"

    def speaks(name):
        print(name.speaks)

    def eats(name, amount):
        name.weight = amount



fido = Dog("fido")
fluffy = Cat("fluffy")

fido.eats(100)

fido.speak()
fluffy.speak()