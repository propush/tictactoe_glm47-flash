#!/usr/bin/env python3
"""
Simple Tic-Tac-Toe game played against the computer.
Run with: python3 tic_tac_toe.py
"""

import sys
import curses
import time
import threading
import json
import os

# Force colorama init for proper ANSI handling
try:
    from colorama import init
    init()
except ImportError:
    pass  # colorama not available, will use raw ANSI

# Save file for persistent scores
SCORE_FILE = "tic_tac_toe_scores.json"


class Difficulty:
    """AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# ANSI Color Codes
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
BOLD = "\033[1m"


class ScoreTracker:
    """Track game scores across multiple sessions with persistent storage."""

    def __init__(self, score_file=None):
        """Initialize score tracker and load scores from file if available.

        Args:
            score_file: Optional path to score file. Defaults to 'tic_tac_toe_scores.json'
        """
        self.score_file = score_file or SCORE_FILE
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.total_games = 0
        self.load_scores()

    def load_scores(self):
        """Load scores from file if it exists."""
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    self.player_wins = data.get('player_wins', 0)
                    self.computer_wins = data.get('computer_wins', 0)
                    self.draws = data.get('draws', 0)
                    self.total_games = data.get('total_games', 0)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or unreadable, start fresh
                self.player_wins = 0
                self.computer_wins = 0
                self.draws = 0
                self.total_games = 0

    def save_scores(self):
        """Save current scores to file."""
        try:
            data = {
                'player_wins': self.player_wins,
                'computer_wins': self.computer_wins,
                'draws': self.draws,
                'total_games': self.total_games
            }
            with open(self.score_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Warning: Could not save scores to file: {e}")

    def record_win(self, player_won, is_draw):
        """Record a win/loss/draw result.

        Args:
            player_won: True if player won
            is_draw: True if game ended in a draw
        """
        self.total_games += 1
        if player_won:
            self.player_wins += 1
        elif is_draw:
            self.draws += 1
        else:
            self.computer_wins += 1
        self.save_scores()  # Auto-save after recording

    def display_scores(self):
        """Display current session statistics."""
        sys.stdout.write("\n" + "=" * 30 + "\n")
        sys.stdout.write("📊 SESSION STATISTICS\n")
        sys.stdout.write("=" * 30 + "\n")
        sys.stdout.write(f"Player wins:      {self.player_wins}\n")
        sys.stdout.write(f"Computer wins:    {self.computer_wins}\n")
        sys.stdout.write(f"Draws:            {self.draws}\n")
        sys.stdout.write(f"Total games:      {self.total_games}\n")
        sys.stdout.write("=" * 30 + "\n")
        sys.stdout.flush()


def get_random_move(board):
    """Get a random valid move from the board."""
    available_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                available_moves.append((i, j))
    import random
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
        if i < 2:
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
        new_row = min(2, cursor_row + 1)
    elif direction == 'left':
        new_col = max(0, cursor_col - 1)
    elif direction == 'right':
        new_col = min(2, cursor_col + 1)

    return new_row, new_col


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
        # Bold effect using A_BOLD attribute
    except:
        # If color initialization fails, continue without colors
        pass

    while True:
        # Clear previous cursor
        stdscr.clear()
        stdscr.refresh()

        # Display board with cursor
        board_display = [[board[i][j] for j in range(3)] for i in range(3)]
        board_display[cursor_row][cursor_col] = 'X'

        for i, row in enumerate(board_display):
            row_str = " | ".join(row)
            if i == cursor_row and cursor_row < 3:
                # Highlight cursor row with colors
                stdscr.addstr(3 + i, 0, row_str, curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(3 + i, 0, row_str, curses.color_pair(1))
            if i < 2:
                stdscr.addstr(4 + i, 0, "-" * 9, curses.color_pair(1))

        # Display instructions
        cursor_pos = f"Cursor at: {cursor_row * 3 + cursor_col + 1}"
        if cursor_row < 3:
            stdscr.addstr(7, 0, cursor_pos, curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(7, len(cursor_pos), "(Use arrow keys to move, Enter to place X)", curses.color_pair(2) | curses.A_BOLD)
        else:
            stdscr.addstr(7, 0, cursor_pos, curses.color_pair(1))
            stdscr.addstr(7, len(cursor_pos), "(Use arrow keys to move, Enter to place X)", curses.color_pair(1))

        stdscr.addstr(8, 0, "Press Ctrl+C to cancel or 'q' to quit", curses.color_pair(1))
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


def check_winner(board, player):
    """Check if the given player has won."""
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board):
    """Check if the board is full."""
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))


def computer_move_easy(board):
    """Easy AI: Makes completely random valid moves."""
    move = get_random_move(board)
    if move:
        board[move[0]][move[1]] = 'O'
    return move


def computer_move_medium(board):
    """Medium AI: Basic strategy (win/block/center/corner/side)."""
    # Try to win
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                if check_winner(board, 'O'):
                    return
                board[i][j] = ' '

    # Try to block player
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                if check_winner(board, 'X'):
                    board[i][j] = 'O'
                    return
                board[i][j] = ' '

    # Take center if available
    if board[1][1] == ' ':
        board[1][1] = 'O'
        return

    # Take a random corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for i, j in corners:
        if board[i][j] == ' ':
            board[i][j] = 'O'
            return

    # Take a random side
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for i, j in sides:
        if board[i][j] == ' ':
            board[i][j] = 'O'
            return


def minimax(board, depth, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning.

    Args:
        board: Current board state
        depth: Current depth in search tree
        maximizing_player: True if computer (O), False if player (X)

    Returns:
        Best score (1 for win, -1 for loss, 0 for draw)
    """
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_full(board):
        return 0

    if maximizing_player:
        max_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_score = max(max_score, score)
        return max_score
    else:
        min_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_score = min(min_score, score)
        return min_score


def computer_move_hard(board):
    """Hard AI: Minimax algorithm for perfect play."""
    best_score = -float('inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
    return best_move


def computer_move(board, difficulty):
    """
    Computer move dispatcher based on difficulty level.

    Args:
        board: The current board state (modified in place)
        difficulty: Difficulty level ('easy', 'medium', or 'hard')
    """
    if difficulty == '1':
        computer_move_easy(board)
    elif difficulty == '2':
        computer_move_medium(board)
    elif difficulty == '3':
        computer_move_hard(board)


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

            row = (move - 1) // 3
            col = (move - 1) % 3

            if board[row][col] != ' ':
                print("That position is already taken!")
                continue

            return row, col
        except ValueError:
            print("Please enter a valid number.")


def play_game():
    """Main game loop."""
    # Initialize score tracker
    score_tracker = ScoreTracker()

    while True:
        # Display current scores at the start of each game
        score_tracker.display_scores()

        print("Welcome to Tic-Tac-Toe!")
        print("You are X, Computer is O")
        print("Number positions: 1 2 3")
        print("                  4 5 6")
        print("                  7 8 9")

        # Difficulty selection
        print("\nSelect difficulty:")
        print("1 - Easy (random moves)")
        print("2 - Medium (basic strategy)")
        print("3 - Hard (perfect play)")
        difficulty = None
        while difficulty not in ['1', '2', '3']:
            choice = input("Enter your choice (1-3): ").lower()
            if choice == '1':
                difficulty = '1'
            elif choice == '2':
                difficulty = '2'
            elif choice == '3':
                difficulty = '3'
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        player_won = False
        # Initialize game state
        board = [[' ' for _ in range(3)] for _ in range(3)]
        player = 'X'
        computer = 'O'
        game_over = False

        while not game_over:
            print_board(board)

            if player == 'X':
                row, col = get_player_move(board)
                board[row][col] = player
                print(f"\nYou placed X at position {row * 3 + col + 1}")

                if check_winner(board, player):
                    print_board(board)
                    print("🎉 Congratulations! You win!")
                    player_won = True
                    game_over = True
                elif is_full(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                    player_won = None
                else:
                    player = 'O'
            else:
                print("\nComputer is thinking...")
                computer_move(board, difficulty)
                print(f"Computer placed O")

                if check_winner(board, computer):
                    print_board(board)
                    print("😔 Computer wins!")
                    game_over = True
                    player_won = False
                elif is_full(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                    player_won = None
                else:
                    player = 'X'

        # Record the result
        score_tracker.record_win(player_won, player_won is None)

        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            score_tracker.display_scores()
            break


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)