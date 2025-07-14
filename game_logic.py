# game_logic.py
# this file contains the core mechanics of the Connect Four game
# board initialization
# making a move
# checking valid locations
# checking for a win
# printing the board (useful for debugging)

import numpy as np
from config import ROW_COUNT, COLUMN_COUNT


def create_board():
    """
    Create a blank Connect Four board using a NumPy 2D array.
    0 represents an empty cell
    1 represents Player 1
    2 represents Player 2
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    """
    Place a player's piece in the specified row and column.
    'piece' is 1 or 2 (player ID).
    """
    board[row][col] = piece


def is_valid_location(board, col):
    """
    Returns true is a piece can be dropped in the given column.
    Columns are valid until the top cell is no longer zero.
    """
    # bug correction: we need to add a check for column bounds
    if col < 0 or col >= COLUMN_COUNT:
        return False

    return board[ROW_COUNT - 1][col] == 0


# bug correction: we need a function to get valid locations
def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]


# bug correction: we might need an optional function for board copying
def copy_board(board):
    return board.copy()


def get_next_open_row(board, col):
    """
    Finds the next available row in the specified column (bottom to top).
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

    return None  # should not happen if this function is called after is_valid_location


def print_board(board):
    """
    Prints the board in a readable format (flipped so the bottom row is at the bottom).
    Useful for debugging in terminal.
    """
    print(np.flip(board, 0))


def winning_move(board, piece):
    """
    Check if the current board state is a win for the given player.
    A win is defined as 4 in a row and can be:
        horizonal
        vertical
        diagonal
    """

    # --- check horizonal wins ---
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # --- check vertical wins ---
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # --- check positive slope diagonals / ---
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # --- check negative slope diagonals \ ---
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False
