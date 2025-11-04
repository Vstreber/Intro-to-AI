import chess
import random

def search(yourColor, board, depth=0, max_depth=3):
    
    bestScore = float('-inf')
    bestScore = -1 
    bestMove = None

    if depth >= max_depth:
        return [0,None]

    legalMoves = list(board.legal_moves)
    random.shuffle(legalMoves)

    for i in legalMoves:
        
        score = 0

        #calculate move score
        score = assignValue(i, board, yourColor)

        #updates board state with new move.
        board.push(i)
        
        #recursion
        score_and_move = search(yourColor, board, depth + 1, max_depth)
        score += score_and_move[0]
        
        board.pop()
        
        #if score is larger, updates bestScore
        if score > bestScore:
            bestScore = score

            bestMove = i

        #debug(i, board, bestScore, score)
    return [bestScore,bestMove]
        
def assignValue(i,board,yourColor):

    score = 0;
    #determining start and end square of move
    startSquare = (str(i))[:2]
    endSquare = (str(i))[-2:]

    #determining value of each captured piece
    if board.is_capture(i):
        # Queen
        if (board.piece_type_at(chess.parse_square(endSquare)) == 5):
            if (board.piece_type_at(chess.parse_square(startSquare)) == yourColor):
                score += 10
            else:
                score -= 10

        # King
        if (board.piece_type_at(chess.parse_square(endSquare)) == 6):
            if (board.piece_type_at(chess.parse_square(startSquare)) == yourColor):
                score += 10
            else:
                score -= 10

        # Knight
        if (board.piece_type_at(chess.parse_square(endSquare)) == 2):         
            if (board.piece_type_at(chess.parse_square(startSquare)) == yourColor):
                score += 5
            else:
                score -= 5

        # Bishop
        if (board.piece_type_at(chess.parse_square(endSquare)) == 3):
            if (board.piece_type_at(chess.parse_square(startSquare)) == yourColor):
                score += 8
            else:
                score -= 8

        # Rook
        if (board.piece_type_at(chess.parse_square(endSquare)) == 4):
            if (board.piece_type_at(chess.parse_square(startSquare)) == yourColor):
                score += 6
            else:
                score -= 6

        # Pawn
        if (board.piece_type_at(chess.parse_square(endSquare)) == 1):
            if (board.piece_type_at(chess.parse_square(startSquare)) == yourColor):
                score += 1
            else:
                score -= 1

    return score

def debug(i, board, bestScore, score):

    print("Move: " + str(i))
    print("Move stack: " + str(board.move_stack))
    #print("Score: " + str(score))
    #print("Best score: " + str(bestScore))
    print("Best move: " + str(i))
