"""Board operations and utilities for Tic-Tac-Toe game."""

import sys
import random
from .constants import (
    BOARD_SIZE,
    RESET,
    GREEN,
    YELLOW,
    BOLD,
    DIM,
    GRID_H,
    GRID_V,
)


def get_random_move(board):
    """Get a random valid move from the board.

    Args:
        board: Current board state

    Returns:
        Tuple of (row, col) or None if no moves available
    """
    available_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                available_moves.append((i, j))
    return random.choice(available_moves) if available_moves else None


def print_board(board, cursor_row=None, cursor_col=None, last_move=None, winning_line=None, show_labels=False):
    """Print the current board state with optional cursor highlighting.

    Args:
        board: Current board state
        cursor_row: Row position of cursor (0-2), or None for no cursor
        cursor_col: Column position of cursor (0-2), or None for no cursor
        last_move: Tuple of (row, col) for last move, or None
        winning_line: List of (row, col) tuples for winning line, or None
        show_labels: Whether to show faint 1-9 labels on empty cells
    """
    rule = GRID_H * 9
    win_set = set(winning_line or [])
    last_move = last_move if last_move is None else tuple(last_move)

    sys.stdout.write("\n" + rule + "\n")
    for i, row in enumerate(board):
        row_str = []
        for j, cell in enumerate(row):
            label = str(i * BOARD_SIZE + j + 1)
            display = cell if cell != ' ' else (label if show_labels else ' ')
            styled = display

            if (i, j) in win_set:
                styled = f"{BOLD}{GREEN}{display}{RESET}"
            elif cursor_row is not None and i == cursor_row and j == cursor_col:
                styled = f"{BOLD}{YELLOW}{display}{RESET}"
            elif last_move is not None and (i, j) == last_move:
                styled = f"{DIM}{display}{RESET}"

            row_str.append(styled)
        sys.stdout.write(f" {GRID_V} ".join(row_str) + "\n")
        if i < BOARD_SIZE - 1:
            sys.stdout.write(rule + "\n")
    sys.stdout.write(rule + "\n")
    sys.stdout.flush()


def move_cursor(cursor_row, cursor_col, direction, board):
    """Move the cursor in the specified direction.

    Args:
        cursor_row: Current cursor row position
        cursor_col: Current cursor column position
        direction: 'up', 'down', 'left', or 'right'
        board: Current board state (to prevent moving into occupied cells)

    Returns:
        New cursor position as (row, col)
    """
    new_row, new_col = cursor_row, cursor_col

    if direction == 'up':
        new_row = max(0, cursor_row - 1)
    elif direction == 'down':
        new_row = min(BOARD_SIZE - 1, cursor_row + 1)
    elif direction == 'left':
        new_col = max(0, cursor_col - 1)
    elif direction == 'right':
        new_col = min(BOARD_SIZE - 1, cursor_col + 1)

    return new_row, new_col
