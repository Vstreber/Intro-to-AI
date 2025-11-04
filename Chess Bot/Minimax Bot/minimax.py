import datetime
import chess
import chess.svg
import minimaxLib

#update the file board.svg to display current board state.
def updateBoard():
    boardsvg = chess.svg.board(board)
    outputfile = open('board.svg', "w")
    outputfile.write(boardsvg)
    outputfile.close()

#initialize board.
board = chess.Board()
updateBoard()

#display date and time.
now = datetime.datetime.now()
print(now)

print("What's your color? (w=white/b=black): ")
color = input()
x = True

while x:
    if(color == "w"):
        computer = "b"
        x = False
    elif(color == "b"):
        computer = "w"
        x = False
    else:
        print("Please enter 'w' or 'b'")
        color = input()

current_player = "w"
human = color

print("Please enter your starting position.")
starting_position = input()
if(starting_position == ""):
    starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

board.set_fen(starting_position)

print(board)
while (board.is_checkmate() == False):
    if human == current_player:
        move = input("Enter your move: ")
        board.push_uci(move)
        if (current_player == "b"):
            current_player = "w"
        else:
            current_player = "b"

        updateBoard()

    elif computer == current_player:
        if (computer == "b"):
            compColor = chess.BLACK
        else:
            compColor = chess.WHITE
        score_and_move = minimaxLib.search(compColor, board)
        print("The bot's move is: " + str(score_and_move[1]))
        board.push_uci(str(score_and_move[1]))

        if (current_player == "b"):
            current_player = "w"
        else:
            current_player = "b"

        updateBoard()

    print("New Fen Position: " + board.fen())

    if board.is_checkmate() == True:
        print("Checkmate!")


