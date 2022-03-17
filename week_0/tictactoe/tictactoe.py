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
    x = 0
    o = 0 
    empty = 0
    
    for row in board:
        for place in row:
            if place == X:
                x += 1
                    
            elif place == O:
                o += 1 
            
            elif place == EMPTY:
                empty += 1
                
    if empty == 9:
        return X
        
    if x == o:
        return X
        
    if x > o and x - o == 1:
        return O
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    
    for row in range(len(board)):
        for place in range(len(board[row])):
            
            if board[row][place] == EMPTY:
                possible.add((row, place))
                
    return possible
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    row = action[0]
    place = action[1]
    result = copy.deepcopy(board)
    
    if action not in actions(board):
        raise ValueError("not a valid action")
        
    else:
        if player(board) == X:
            result[row][place] = X
            
        else:
            result[row][place] = O
    
    # for i in range(len(result)):
    #   print(result[i])
    # print(" ")
    
    return result
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x = 0 
    o = 0
    
    for row in board:
        for place in row:
            if place == X:
                x += 1
            if place == O:
                o += 1
                
            if x == 3:
                return X
            elif o == 3:
                return O
        else:
            x = 0
            o = 0
                
    for i in range(len(board)):
        for row in board:
            if row[i] == X:
                x += 1
            if row[i] == O:
                o += 1
                
            if x == 3:
                return X
            elif o == 3:
                return O
        else:
            x = 0
            o = 0
    
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
            
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O 
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
        
    empty = 0
    
    for row in board:
        for place in row:
            if place == EMPTY:
                empty += 1
    
    if empty == 0:
        return True
        
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
        

def minimax_helper_X(board):
    
    if terminal(board) == True:
        return utility(board)
    
    high = -1
    for action in actions(board):
        
        next_board = result(board, action)
        
        if minimax2(next_board) > high:
            high = minimax2(next_board)
            
    return high 
        
                     
def minimax_helper_O(board):
    
    if terminal(board) == True:
        return utility(board)
    
    low = 1
    for action in actions(board):
        
        next_board = result(board, action)
        
        if minimax2(next_board) < low:
            low = minimax2(next_board)
            
    return low 
        

def minimax2(board):
    
    if player(board) == X:
        return minimax_helper_X(board)
            
    if player(board) == O:
        return minimax_helper_O(board)
    
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
        
    if player(board) == X:
        # to speed up the first move 
        empty = 0
    
        for row in board:
            for place in row:
                if place == EMPTY:
                    empty += 1
                    
        if empty == 9:
            return (0, 1)
        
        help_list = []
        for action in actions(board):
            
            next_board = result(board, action)
            help_list.append((minimax2(next_board), action))
            
        for action in range(len(actions(board))):
            if help_list[action][0] == 1:
                return help_list[action][1]
                
        for action in range(len(actions(board))):
            if help_list[action][0] == 0:
                return help_list[action][1]        
        
    if player(board) == O:
        
        help_list = []
        for action in actions(board):
            
            next_board = result(board, action)
            help_list.append((minimax2(next_board), action))
        
        for action in range(len(actions(board))):
            if help_list[action][0] == -1:
                return help_list[action][1] 
                
        for action in range(len(actions(board))):
            if help_list[action][0] == 0:
                return help_list[action][1] 

    return None