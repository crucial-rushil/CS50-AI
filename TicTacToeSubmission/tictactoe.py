"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for i in range(3):
        for j in range(3):
            if (board[i][j] == X):
                x_count = x_count+1
            elif (board[i][j] == O):
                o_count = o_count +1

    if ((x_count + o_count)%2 == 1):
        return O
    return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                action = (i,j)
                moves.add(action)
    return moves
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("The state is not valid.")

    copy_board = copy.deepcopy(board)
    turn = player(board)
    copy_board[action[0]][action[1]] = turn
    return copy_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check for if x is a winner (8 cases)

    #Case 1 (Rows)
    for i in range(0, len(board)):
        if (board[i] == [X, X, X]):
            return X
        elif (board[i] == [O, O, O]):
            return O

    #Case 2 (Cols)
    temp = []
    for i in range(0,len(board)):
        for j in range(0,3):
            temp.append(board[j][i])

        if (temp == [X, X, X]):
            return X
        elif (temp == [O, O, O]):
            return O
        temp.clear()



    #Case 3 (Diagonals)
    #Top Left to Bottom Right
    temp2 = []
    for i in range(3):
        for j in range(3):
            if (i == j):
                temp2.append(board[i][j])

    if (temp2 == [X, X, X]):
        return X
    elif (temp2 == [O, O, O]):
        return O

    #Bottom Left to Top Right
    temp3 = []
    for i in range(2,-1,-1):
        for j in range(3):
            if (i + j == 2):
                temp3.append(board[i][j])

    if (temp3 == [X, X, X]):
        return X
    elif (temp3 == [O, O, O]):
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (utility(board) == 1 or utility(board) == 0 or utility(board) == -1):
        return True

    return False

    #return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise if in a tie.
    """
    if winner(board) is X:
        return 1
    elif winner(board) is O:
        return -1
    else:
        checker = True
        for i in range(3):
            for j in range(3):
                if (board[i][j] == EMPTY):
                    checker = False
                    break

        if(checker == True):
            return 0
    return -5

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if (board == initial_state()): #randomize first starting pos if AI is "X"
        return (0,0)
    number, move = helper(board, player(board))
    return move

    raise NotImplementedError



def helper(board,players): #assume the AI is the "X" and try to maximize

    if (terminal(board)):
        return utility(board), None

    if (player(board) == "X"):
        mAxvalue = -100000
        move1 = None
        for action in actions(board):
            val, act = helper(result(board,action),"O")
            if (val > mAxvalue):
                mAxvalue = val
                move1 = action

        return mAxvalue, move1

    elif (player(board) == "O"):
        value = 100000
        move2 = None
        for action in actions(board):
            val2, act2 = helper(result(board,action), "O")
            if (val2 < value):
                value = val2
                move2 = action


        return value, move2
