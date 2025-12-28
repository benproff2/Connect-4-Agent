import numpy as np

ROWS = 6
COLS = 7


def create_board():
    """Creates a 6x7 Connect 4 board using a numpy 2D array that is filled with zeros

    Returns:
        A 6x7 array representing the game board
    """
    return np.zeros((ROWS, COLS), dtype=int)



def print_board(board):
    """Print the current state of the board, displaying the bottom row at the bottom

    Args:
        board: The current game board 
    """
    print("\n  " + "  ".join(str(c) for c in range(COLS)))  # column headers

    for row in board:
        print("| " + "  ".join(str(cell) if cell != 0 else "." for cell in row) + " |")  # '.' means it's an empty cell



def is_valid_location(board, col):
    """Check if the top cell of a column is empty (which is a valid move)

    Args:
        board: the current game board
        col: column check to check

    Returns:
        True if the column has space, and False otherwise
    """
    if col < 0 or col >= COLS:
        return False
    
    return board[0][col] == 0



def get_next_open_row(board, col):
    """Find the next available row in a given column to drop a piece
    
    Args:
        board: The current game board
        col: Column index to check
    
    Returns:
        The row index where the piece can be placed
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
        


def drop_piece(board, row, col, player):
    """Drop a player's piece into the board at the given location
    
    Args:
        board: The current game board
        row: The row index to place the piece
        col: The column index to place the piece
        player: The player number (1 or 2)
    """
    board[row][col] = player
    return board



def check_win(board, player):
    """Check whether the given player has won the game by having 4 in a row
    
    Args:
        board: The current game board
        player: The player number to check for a win
    
    Returns:
        True if the player has a winning condition, and False otherwise
    """
    # horizontal win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r, c+i] == player for i in range(4)):
                return True
            
    # vertical win
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i, c] == player for i in range(4)):
                return True
            
    # positive diagonal win
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i, c+i] == player for i in range(4)):
                return True
            
    # negative diagonal win
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i, c+i] == player for i in range(4)):
                return True
            
    # return False if a player does not have a winning condition        
    return False



def is_draw(board):
    """Check if the board is full, resulting in a draw
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full with no winner, and False otherwise
    """
    return all(board[0][c] != 0 for c in range(COLS))



def get_children(board, player):
    """Generates all possible child board states resulting from the current player's valid moves

    Args:
        board: The current game board
        player: The player number (either 1 or 2) making the move

    Returns:
        A list of a new board states after each possible valid move
    """
    children = []
    for c in range(COLS):
        if is_valid_location(board, c):
            row = get_next_open_row(board, c)
            new_board = board.copy()
            drop_piece(new_board, row, c, player)
            children.append(new_board)
            
    return children