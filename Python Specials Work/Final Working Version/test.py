import TicTacToe as TTT

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

def player_setup():
    PLAYER_ONE_NAME = input("PLAYER ONE: Enter your name...\t")
    message = PLAYER_ONE_NAME + " : Choose 'O' or 'X'\t"
    PLAYER_ONE_CHAR = input(message).upper()
    # check they entered X or O, if not re-prompt
    if PLAYER_ONE_CHAR == 'X':
        PLAYER_TWO_CHAR = 'O'
    elif PLAYER_ONE_CHAR == 'O':
        PLAYER_TWO_CHAR = 'X'
    else:
        print("Idjit,PLAYER ONE is X...")
        PLAYER_ONE_CHAR = 'X'
        PLAYER_TWO_CHAR = 'O'
    PLAYER_TWO_NAME = input("PLAYER TWO: Enter your name...\t")
    p1 = Player(PLAYER_ONE_NAME, PLAYER_ONE_CHAR)
    p2 = Player(PLAYER_TWO_NAME, PLAYER_TWO_CHAR)
    return p1, p2

def game(player_details, board):
    for i in range(9):  # no more than 9 moves possible
        move = loop_until_move_valid(player_details[i % 2])
        print(move)
        msg = make_move(move, board)[1]
        print(msg)
        if "has won" in msg:
            break

def entered_move_is_valid(m):
    return len(m) == 1 and m.isdigit() and int(m) != 0

def loop_until_move_valid(user):
    user_move = input(user.name + ": Choose a position from 1 - 9...\t")
    if not entered_move_is_valid(user_move):
        while True:
            print("Try again...\t")
            user_move = input(user.name + ": Choose a position from 1 - 9...\t")
            if entered_move_is_valid(user_move):
                break
    return int(user_move),user.symbol

def make_move(move, board):
    while True:
        result_of_move = board.play(move)
        if result_of_move[0]:
            break
        else:
            print("Invalid move, please pick an *empty* slot...")
            move = loop_until_move_valid(Player("errorPlayer", move[1]))
    #board.describe()
    board.niceDescribe()
    return result_of_move


# loop_until_char_valid()





    
#game(player_setup())

gameBoard = TTT.Board()
players = player_setup()
game(players, gameBoard)
