class Board:
    initial_state = [" ", " ", " ",
                     " ", " ", " ",
                     " ", " ", " "]

    def __init__(self):
        self.current_state = [None, None, None,
                              None, None, None,
                              None, None, None]

        self.game_play = []

        pass

    def describe(self):
        print("\n")
        print(self.current_state[0], "#", self.current_state[1], "#", self.current_state[2])
        print("##### ##### #####")
        print(self.current_state[3], "#", self.current_state[4], "#", self.current_state[5])
        print("##### ##### #####")
        print(self.current_state[6], "#", self.current_state[7], "#", self.current_state[8], "\n", "\n")

    def niceDescribe(self):
        str = "\n"
        for row in range (3):
            for col in range(3):
                str += " " + self.current_state[3*row + col] if self.current_state[3*row + col] else " " + " "
                str += " #" if col < 2 else "\n"
            str += "### ### ###\n" if row < 2 else "\n"
        print(str)

    def reset(self):
        pass

    def input_valid(self, move):

        if type(move[0]) is int and move[0] - 1 in range(9):
            if type(move[1]) is str and len(move[1]) == 1:
                return True, "input valid"
            else:
                return False, "input invalid: more than one char entered as player"
        else:
            return False, "input invalid: grid square out of range"

    def play_valid(self, play):

        if self.current_state[play[0]] is None:
            return True, "play is valid"
        else:
            return False, "move invalid, space occupied"

    def make_change(self, change):

        self.current_state[change[0]] = change[1]
        return True

    def play(self, user_input):

        # converting the user_input tuple from player into user_input list.
        user_input = [user_input[0], user_input[1]]

        if self.input_valid(user_input)[0]:

            # Adjusting for the list index which is 0-8.
            user_input[0] -= 1

            if self.play_valid(user_input)[0]:

                self.game_play += [user_input]
                self.make_change(user_input)
                return self.game_won()
                #return True, "user input and play valid, move recorded"

            else:
                return False, "play invalid, please enter a valid move"
        else:
            return False, "input invalid, please enter values in range"

    def game_won(self):

        for i in range(9):

            if self.current_state[i] is None:
                return True, "didn't win yet"

            if i % 3 == 0 and self.current_state[i] == self.current_state[i + 1] == self.current_state[i + 2]:
                return True, "{0}, has won".format(self.current_state[i])

            if i < 3 and self.current_state[i] == self.current_state[i + 3] == self.current_state[i + 6]:
                return True, "{0}, has won".format(self.current_state[i])

            if self.current_state[0] is not None and self.current_state[0] == self.current_state[4] == self.current_state[8]:
                return True, "{0}, has won".format(self.current_state[0])

            if self.current_state[2] is not None and self.current_state[2] == self.current_state[4] == self.current_state[6]:
                return True, "{0}, has won".format(self.current_state[2])

