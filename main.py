# main.py
# this file...
# initializes the game window and board
# listens for player input
# alternates turns between the player and the AI
# uses the minimax AI to bring in decision-making
# calls GUI functions to draw the board and display results

import pygame
import sys
import numpy as np
from config import *
from game_logic import (
    create_board,
    drop_piece,
    is_valid_location,
    get_next_open_row,
    winning_move,
    print_board,
)
from minimax_ai import minimax
from minimax_ai import PLAYER_PIECE, AI_PIECE
from gui import draw_board, show_winner

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect Four: Human vs. AI")
font = pygame.font.SysFont("monospace", FONT_SIZE)

board = create_board()
draw_board(screen, board)
pygame.display.update()

# initialize display indicators
game_over = False
turn = 0  # 0 = Human (red), 1 = AI (yellow)

# now start the main loop for the game
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # draw the player's disc as hovering
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        # handle mouse click (player move)
        if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            # first clear the hovering
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))

            posx = event.pos[0]
            col = int(posx / SQUARE_SIZE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    draw_board(screen, board)
                    show_winner(screen, font, "You win!!!", RED)
                    game_over = True

                turn = 1  # now switch it over to the AI
                draw_board(screen, board)

    # now it's the AI's turn
    if turn == 1 and not game_over:
        pygame.time.wait(500)  # make a small delay at the turnover

        col, minimax_score = minimax(board, MAX_DEPTH, -np.inf, np.inf, True)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                draw_board(screen, board)
                show_winner(screen, font, "Oh no, the AI won...", YELLOW)
                game_over = True

            draw_board(screen, board)
            turn = 0  # switch back to the human player

    # end game delay
    if game_over:
        pygame.time.wait(3000)
