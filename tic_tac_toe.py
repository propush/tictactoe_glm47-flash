#!/usr/bin/env python3
"""
Simple Tic-Tac-Toe game played against the computer.
Run with: python3 tic_tac_toe.py
"""

import sys


class Difficulty:
    """AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ScoreTracker:
    """Track game scores across multiple sessions."""
    def __init__(self):
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.total_games = 0

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

    def display_scores(self):
        """Display current session statistics."""
        print("\n" + "=" * 30)
        print("📊 SESSION STATISTICS")
        print("=" * 30)
        print(f"Player wins:      {self.player_wins}")
        print(f"Computer wins:    {self.computer_wins}")
        print(f"Draws:            {self.draws}")
        print(f"Total games:      {self.total_games}")
        print("=" * 30)


def get_random_move(board):
    """Get a random valid move from the board."""
    available_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                available_moves.append((i, j))
    import random
    return random.choice(available_moves) if available_moves else None


def print_board(board):
    """Print the current board state."""
    print("\n" + "=" * 9)
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)
    print("=" * 9 + "\n")


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
    """Get valid move from player."""
    while True:
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