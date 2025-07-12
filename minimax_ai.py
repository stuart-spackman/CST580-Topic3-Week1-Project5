# minimax_ai.py
# implements Minimax algorithm with Alpha-Beta pruning and a heuristic evaluation function
# this is the file where the AI "thinks" about its next move
# this file includes:
# the minimax algorithm with alpha-beta pruning
# a board scoring function (for heuristic evaluation)
# a function to find the best move for the AI

import math
import random
import numpy as np
from config import ROW_COUNT, COLUMN_COUNT, MAX_DEPTH
from game_logic import get_next_open_row, is_valid_location, drop_piece, winning_move

PLAYER = 0  # human player (assumes piece = 1)
AI = 1  # AI player (assumes piece = 2)
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4  # length of the sequence to evaluate


def evaluate_window(window, piece):
    """
    Scores a group of 4 cells (a 'window') based on how favorable it is to the given piece.
    """
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # now we need to decided on metrics for how good or bad a move is
    if window.count(piece) == 4:
        score += 100  # winning move
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10  # very strong move
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5  # decent move
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80  # block the opponent's strong threat

    return score


def score_position(board, piece):
    """
    We need to be able to evaluate the whole board for the given piece.
    Windows of 4 need to be tried.
    """
    score = 0

    # first score the center column
    center_array = [int(board[r][COLUMN_COUNT // 2]) for r in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += (
        center_count * 6
    )  # we want to think of the center as being strategically strong

    # then score the horizonal config
    for r in range(ROW_COUNT):
        row_array = [int(board[r][c]) for c in range(COLUMN_COUNT)]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # now score the vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(board[r][c]) for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score positive diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # score negative diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # now we can finally return the total score
    return score


def get_valid_locations(board):
    """
    Returns a list of column indices where a move is possible.
    """
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]


def is_terminal_node(board):
    """Returns true if a player wins OR a draw is reached, i.e., game over."""
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE)


def minimax(board, depth, alpha, beta, maximizingPlayer):
    """
    Here we finally call on the minimax algorith.
    This is a recursive version with Alpha-Beta pruning.
    """
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    # first check if the game has come to an end
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
        elif winning_move(board, PLAYER_PIECE):
            return (None, -100000000000000)
        else:
            # this branch means the game is over with no more valid moves (it's a draw)
            return (None, 0)

    # now we need to split the game logic between maximizing player and minimizing player
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            # recursion requires a copy of the board be made
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # this is where the pruning happens

        return best_col, value

    # minimzing player
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            # recursion requires a copy of the board be made
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # another pruning situation

        return best_col, value


def pick_best_move(board, piece):
    """
    I decided to put in an optional helper function.
    This is for a fast heuristic AI without using the full minimax.
    """
    valid_locations = get_valid_locations(board)
    best_score = -math.inf
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col
