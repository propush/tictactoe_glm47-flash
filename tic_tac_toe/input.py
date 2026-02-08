"""Player input handling for Tic-Tac-Toe game."""

import time
import curses
from .board import move_cursor
from .constants import BOARD_SIZE, PLAYER


def get_arrow_move(stdscr, board, last_move=None):
    """Get move using arrow keys and Enter.

    Args:
        stdscr: curses window object for input
        board: Current board state
        last_move: Tuple of (row, col) for last move, or None

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

        # Display board with cursor highlight (no mutation)
        board_top = 3
        row_step = 2
        for i in range(BOARD_SIZE):
            row_y = board_top + i * row_step
            col = 0
            for j in range(BOARD_SIZE):
                is_cursor = i == cursor_row and j == cursor_col
                is_last = last_move is not None and (i, j) == tuple(last_move)
                # Show a visible move preview at the cursor on empty cells.
                if is_cursor and board[i][j] == ' ':
                    cell = PLAYER
                else:
                    cell = board[i][j]
                if is_cursor:
                    attr = curses.color_pair(2) | curses.A_BOLD
                elif is_last:
                    attr = curses.color_pair(1) | curses.A_DIM
                else:
                    attr = curses.color_pair(1)
                stdscr.addstr(row_y, col, cell, attr)
                if j < BOARD_SIZE - 1:
                    stdscr.addstr(row_y, col + 1, " | ", curses.color_pair(1))
                col += 4
            if i < BOARD_SIZE - 1:
                stdscr.addstr(row_y + 1, 0, "-" * 9, curses.color_pair(1))

        # Display instructions
        instructions_y = board_top + BOARD_SIZE * row_step
        cursor_pos = f"Cursor: {cursor_row * BOARD_SIZE + cursor_col + 1}"
        stdscr.addstr(instructions_y, 0, cursor_pos, curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(
            instructions_y,
            len(cursor_pos),
            "  Arrows: move  Enter: place X",
            curses.color_pair(2) | curses.A_BOLD,
        )
        stdscr.addstr(
            instructions_y + 1,
            0,
            "Ctrl+C: cancel  q: quit",
            curses.color_pair(1),
        )
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
                    error_y = instructions_y + 2
                    stdscr.addstr(
                        error_y,
                        0,
                        "Cell already occupied! ",
                        curses.color_pair(3) | curses.A_BOLD,
                    )
                    stdscr.refresh()
                    time.sleep(1)
            # Handle quit command
            elif key == ord('q'):
                return None
        except KeyboardInterrupt:
            return None

        stdscr.clear()
        stdscr.refresh()


def get_player_move(board, last_move=None):
    """Get valid move from player.

    Args:
        board: Current board state
        last_move: Tuple of (row, col) for last move, or None

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

            move = get_arrow_move(stdscr, board, last_move=last_move)

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
            print("Tip: Use arrow keys to move, or enter a number 1-9.")
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
