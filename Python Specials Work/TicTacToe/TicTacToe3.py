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

    def reset(self):
        pass


    def input_valid(self, move):

        #self.move = move

        if type(move[0]) is int and move[0] - 1 in range(9):

            #print(move, "step 1")

            if type(move[1]) is str and len(move[1]) == 1:

                #print(move, "step 2")

                return True, "input valid"

            else:

                return False, "input invalid: more than one char entered as player"

        else:
            #print(move)

            return False, "input invalid: grid square out of range"




    def play_valid(self, play):

        #print(play, "step 3")

        if self.current_state[play[0]] is None:

            #print(play, "step 4")

            return True, "play is valid"

        else:
            #print(play, "step 5")

            return False, "move invalid, space occupied"



    def make_change(self, change):

        self.current_state[change[0]] = change[1]

        #print(change, "step 6")

        return True



    def play(self, user_input):

        #converting the user_input tuple from player into user_input list.
        user_input = [user_input[0], user_input[1]]



        if self.input_valid(user_input)[0]:


            # Adjusting for the list index which is 0-8.
            user_input[0] -= 1

            if self.play_valid(user_input)[0]:

                self.game_play += [user_input]
                self.make_change(user_input)

                return True, "user input and play valid, move recorded"

            else:
                return False, "play invalid, please enter a valid move"

        else:
            return False, "input invalid, please enter values in range"



    def game_won(self):

        for i in range(9):

            if self.current_state[i] is None:

                break


            if i % 3 == 0 and self.current_state[i] == self.current_state[i + 1] == self.current_state[i + 2]:

                return True, "{0}, has won".format(self.current_state[i])

            if i < 3 and self.current_state[i] == self.current_state[i + 3] == self.current_state[i + 6]:

                return True, "{0}, has won".format(self.current_state[i])

            if self.current_state[0] == self.current_state[4] == self.current_state[8]:

                return True, "{0}, has won".format(self.current_state[0])

            if self.current_state[2] == self.current_state[4] == self.current_state[6]:

                return True, "{0}, has won".format(self.current_state[2])




    # def save(self):
    #
    #     with file, open ("C:\\Users\Admin\Desktop\Log.txt", a):
    #
    #         self.game_play
    #
    #






board = Board()
game1 = Board()

#board.describe()

print("Starting State")
game1.describe()




"""Game 1 = 8 moves, O Wins:
    remember that user IO is adjusted by -1 for the location"""

## Move 1
print("Move 1 :", game1.play((1, "X")))
game1.describe()

## Move 2
print("Move 2 :", game1.play((5, "O")))
game1.describe()

## Move 3
print("Move 3 :", game1.play((3, "X")))
game1.describe()

## Move 4
print("Move 4 :", game1.play((2, "O")))
game1.describe()

## Move 5
print("Move 5 :", game1.play((8, "X")))
game1.describe()

## Move 6
print("Move 6 :", game1.play((4, "O")))
game1.describe()

## Move 7
print("Move 7 :", game1.play((9, "X")))
game1.describe()

## Move 8
print("Move 8 :", game1.play((6, "O")))
game1.describe()

print(game1.game_play)







""" Test sequence:
    remember that user IO is adjusted by -1 for the location
    and the program doesnt care what character you have selected
    to represent yourself"""

# ## VALID MOVE
# print("Test 1 :", board.play((1, "X")))
# #board.describe()
#
# ## VALID MOVE
# print("Test 2 :", board.play((9, "X")))
# #board.describe()
#
# ## INVALID MOVE
# print("Test 3 :", board.play(("c", "X")))
# #board.describe()
#
# ## VALID MOVE
# print("Test 4 :", board.play((4, "O")))
# #board.describe()
#
# ## INVALID MOVE
# print("Test 5 :", board.play((5, "2")))
# #board.describe()
#
# ## INVALID MOVE
# print("Test 6 :", board.play(("+", 7)))
# #board.describe()
#
# ## INVALID MOVE
# print("Test 7 :", board.play(("$", "&")))
# #board.describe()
























#
# board1 = Board()
# print
# board1.current_state
#
# board2 = Board()
# print
# board2.current_state
#
# game = Board.describe()