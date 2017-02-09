
class Board:

    initial_state = [" ", " ", " ",
                     " ", " ", " ",
                     " ", " ", " "]



    def __init__(self):

        self.current_state = [" ", " ", " ",
                             " ", " ", " ",
                             " ", " ", " "]


        pass


    def describe(self):

        print(Board.current_state[0], "#", Board.current_state[1], "#", Board.current_state[2])
        print("##### ##### #####")
        print(Board.current_state[3], "#", Board.current_state[4], "#", Board.current_state[5])
        print("##### ##### #####")
        print(Board.current_state[6], "#", Board.current_state[7], "#", Board.current_state[8])




    def reset(self):

        pass



    def play(self, move):

        self.move = move

        if move[0] == None:


            self.current_state[(move[0])].append([move[1]])





        pass


board1 = Board()
print board1.current_state

board2 = Board()
print board2.current_state



game = Board.describe()