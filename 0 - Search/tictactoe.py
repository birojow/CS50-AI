"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

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
    # count X's and O's
    totalX = 0
    totalO = 0
    for row in range(len(board)):
        totalX += board[row].count(X)
        totalO += board[row].count(O)

    if totalX == totalO:
        # same number of moves from both, X's turn
        return X
    else:
        # if not, O's turn (since X starts)
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(3):
        for column in range(3):
            # every EMPTY square is a possible action
            if board[row][column] == EMPTY:
                possible_actions.add((row, column))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_actions = actions(board)

    if action not in possible_actions:
        # if action do not exists, it's an error
        raise IndexError
    else:
        copy_of_board = deepcopy(board)
        (row, column) = action
        # apply the current player move to the board
        copy_of_board[row][column] = player(board)
        return copy_of_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check diagonals, skipping if center is EMPTY
    if board[1][1] != EMPTY:
        if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
            return board[1][1]
    
    # check rows
    for row in range(3):
        if board[row].count(X) == 3:
            return X
        elif board[row].count(O) == 3:
            return O
    
    # check columns
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] and board[0][column] != EMPTY:
            return board[0][column]

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if there is at least one EMPTY square
    no_empty_square = True
    for row in range(len(board)):
        if EMPTY in board[row]:
            no_empty_square = False
            break

    if winner(board) or no_empty_square:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # if current player is X, check the next moves
    # starting with O, and stores the best option
    if player(board) == X:
        best_value = -math.inf
        next_move = set()
        for action in actions(board):
            utility_value = min_value(result(board, action))
            if utility_value > best_value:
                best_value = utility_value
                next_move = action
    # if current player is O, check the next moves
    # starting with X, and stores the best option
    else:
        best_value = math.inf
        next_move = set()
        for action in actions(board):
            utility_value = max_value(result(board, action))
            if utility_value < best_value:
                best_value = utility_value
                next_move = action
    return next_move


def max_value(board):
    """
    Finds the utility value to X move
    """
    if terminal(board): 
        return utility(board)
    
    utility_value = -math.inf
    for action in actions(board):
        utility_value = max(utility_value, min_value(result(board, action)))
    return utility_value


def min_value(board):
    """
    Finds the utility value to O move
    """
    if terminal(board): 
        return utility(board)

    utility_value = math.inf
    for action in actions(board):
        utility_value = min(utility_value, max_value(result(board, action)))   
    return utility_value
