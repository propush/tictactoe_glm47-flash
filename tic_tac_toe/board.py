"""Board operations and utilities for Tic-Tac-Toe game."""

import sys
import random
from .constants import BOARD_SIZE, PLAYER, COMPUTER, RESET, GREEN, BOLD


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


def print_board(board, cursor_row=None, cursor_col=None):
    """Print the current board state with optional cursor highlighting.

    Args:
        board: Current board state
        cursor_row: Row position of cursor (0-2), or None for no cursor
        cursor_col: Column position of cursor (0-2), or None for no cursor
    """
    sys.stdout.write("\n" + "=" * 9 + "\n")
    for i, row in enumerate(board):
        # Build row with possible cursor highlighting
        row_str = []
        for j, cell in enumerate(row):
            if cursor_row is not None and i == cursor_row and j == cursor_col:
                # Highlight cursor position
                highlighted_cell = f"{BOLD}{GREEN}{cell}{RESET}"
                row_str.append(highlighted_cell)
            else:
                row_str.append(cell)
        sys.stdout.write(" | ".join(row_str) + "\n")
        if i < BOARD_SIZE - 1:
            sys.stdout.write("-" * 9 + "\n")
    sys.stdout.write("=" * 9 + "\n")
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


def check_winner(board, player):
    """Check if the given player has won.

    Args:
        board: Current board state
        player: Player marker ('X' or 'O')

    Returns:
        True if player has won
    """
    # Check rows, columns, and diagonals
    for i in range(BOARD_SIZE):
        if all(board[i][j] == player for j in range(BOARD_SIZE)):
            return True
        if all(board[j][i] == player for j in range(BOARD_SIZE)):
            return True
    if all(board[i][i] == player for i in range(BOARD_SIZE)):
        return True
    if all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True
    return False


def is_full(board):
    """Check if the board is full.

    Args:
        board: Current board state

    Returns:
        True if board is full
    """
    return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))


def get_available_moves(board):
    """Get all empty cells on the board.

    Args:
        board: Current board state

    Returns:
        List of (row, col) tuples for empty cells
    """
    return [(i, j) for i in range(BOARD_SIZE)
            for j in range(BOARD_SIZE) if board[i][j] == ' ']


def make_move(board, row, col, player):
    """Place a piece on the board.

    Args:
        board: Current board state (modified in place)
        row: Row position (0-2)
        col: Column position (0-2)
        player: Player marker ('X' or 'O')

    Returns:
        True if move was successful
    """
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False