# config.py
# this file contains configuration constants needed to create a Connect Four game board
# we need consistent styling and behavior across all components

# --- Board Dimensions ---
ROW_COUNT = 6
COLUMN_COUNT = 7

# --- Colors (RGB) ---
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # player 1 (human)
YELLOW = (255, 255, 0)  # player 2 (AI)

# --- Pygame Window Settings ---
SQUARE_SIZE = 100  # size of one cell in pixels
RADIUS = int((SQUARE_SIZE / 2) - 5)

# --- Calculated Screen Size ---
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE  # extra row for user input
size = (width, height)

# font size
FONT_SIZE = 60

# --- AI Settings ---
MAX_DEPTH = 5  # search depth for the Minimax algorithm
