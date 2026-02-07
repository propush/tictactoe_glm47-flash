"""Player input handling for Tic-Tac-Toe game."""

import sys
import time
import curses
from .board import move_cursor, BOARD_SIZE, PLAYER, COMPUTER, get_available_moves
from .constants import RESET, GREEN, RED, BOLD


def get_arrow_move(stdscr, board):
    """Get move using arrow keys and Enter.

    Args:
        stdscr: curses window object for input
        board: Current board state

    Returns:
        Tuple of (row, col) if move made, or None
    """
    cursor_row, cursor_col = 0, 0  # Start at top-left

    # Initialize colors for curses
    try:
        curses.start_color()
        curses.use_default_colors()
        # Define color pairs: (pair_number, fg_color, bg_color)
        # White for normal text
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Green for highlighted text
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Red for error text
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    except:
        # If color initialization fails, continue without colors
        pass

    while True:
        # Clear previous cursor
        stdscr.clear()
        stdscr.refresh()

        # Display board with cursor
        board_display = [[board[i][j] for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        board_display[cursor_row][cursor_col] = PLAYER

        for i, row in enumerate(board_display):
            row_str = " | ".join(row)
            if i == cursor_row and cursor_row < BOARD_SIZE:
                # Highlight cursor row with colors
                stdscr.addstr(3 + i, 0, row_str, curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(3 + i, 0, row_str, curses.color_pair(1))
            if i < BOARD_SIZE - 1:
                stdscr.addstr(4 + i, 0, "-" * 9, curses.color_pair(1))

        # Display instructions
        cursor_pos = f"Cursor at: {cursor_row * BOARD_SIZE + cursor_col + 1}"
        if cursor_row < BOARD_SIZE:
            stdscr.addstr(7, 0, cursor_pos, curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(7, len(cursor_pos),
                         "(Use arrow keys to move, Enter to place X)",
                         curses.color_pair(2) | curses.A_BOLD)
        else:
            stdscr.addstr(7, 0, cursor_pos, curses.color_pair(1))
            stdscr.addstr(7, len(cursor_pos),
                         "(Use arrow keys to move, Enter to place X)",
                         curses.color_pair(1))

        stdscr.addstr(8, 0, "Press Ctrl+C to cancel or 'q' to quit",
                     curses.color_pair(1))
        stdscr.refresh()

        # Get input
        try:
            key = stdscr.getch()

            # Handle arrow keys
            if key == curses.KEY_UP:
                cursor_row, cursor_col = move_cursor(cursor_row, cursor_col, 'up', board)
            elif key == curses.KEY_DOWN:
                cursor_row, cursor_col = move_cursor(cursor_row, cursor_col, 'down', board)
            elif key == curses.KEY_LEFT:
                cursor_row, cursor_col = move_cursor(cursor_row, cursor_col, 'left', board)
            elif key == curses.KEY_RIGHT:
                cursor_row, cursor_col = move_cursor(cursor_row, cursor_col, 'right', board)
            # Handle Enter key to place move
            elif key == ord('\n') or key == curses.KEY_ENTER:
                if board[cursor_row][cursor_col] == ' ':
                    return cursor_row, cursor_col
                else:
                    # Show error message
                    stdscr.addstr(7, 0, "Cell already occupied! ", curses.color_pair(3) | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(1)
            # Handle quit command
            elif key == ord('q'):
                return None
        except KeyboardInterrupt:
            return None

        stdscr.clear()
        stdscr.refresh()


def get_player_move(board):
    """Get valid move from player.

    Args:
        board: Current board state

    Returns:
        (row, col) tuple of player's move
    """
    while True:
        # Try arrow key input first
        try:
            stdscr = curses.initscr()
            stdscr.nodelay(0)  # Make getch blocking
            stdscr.keypad(True)
            stdscr.clear()
            stdscr.refresh()

            move = get_arrow_move(stdscr, board)

            if move is not None:
                curses.endwin()
                return move
            curses.endwin()
        except Exception:
            try:
                curses.endwin()
            except:
                pass

        # Fall back to number input
        try:
            move = input("Enter your move (1-9): ")
            move = int(move)

            if move < 1 or move > 9:
                print("Please enter a number between 1 and 9.")
                continue

            row = (move - 1) // BOARD_SIZE
            col = (move - 1) % BOARD_SIZE

            if board[row][col] != ' ':
                print("That position is already taken!")
                continue

            return row, col
        except ValueError:
            print("Please enter a valid number.")