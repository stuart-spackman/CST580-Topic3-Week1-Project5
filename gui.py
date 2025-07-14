# gui.py
# this file handles all the drawing logic
# draw_board refreshes visual
# show_winner announces the game result

# imports
import pygame
import sys
import numpy as np
from config import *
from minimax_ai import PLAYER_PIECE, AI_PIECE


def draw_board(screen, board):
    """
    draws the connect four board
    discs are colored based on game state
    """
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # first draw a blue grid
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )
            # empty slots get drawn as black circles
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                    int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2),
                ),
                RADIUS,
            )

    # now we can draw the pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                        HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                        HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()


def show_winner(screen, font, text, color):
    """
    To finalize things we need to be able to display a game over message at the top of the screen.
    """
    label = font.render(text, True, color)
    screen.blit(label, (40, 10))
    pygame.display.update()
