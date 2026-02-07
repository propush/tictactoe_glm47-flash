"""AI opponent logic and minimax algorithm for Tic-Tac-Toe game."""

import sys
import random
from .board import check_winner, is_full, get_random_move, BOARD_SIZE, PLAYER, COMPUTER


def computer_move_easy(board):
    """Easy AI: Makes completely random valid moves.

    Args:
        board: Current board state (modified in place)
    """
    move = get_random_move(board)
    if move:
        board[move[0]][move[1]] = COMPUTER


def computer_move_medium(board):
    """Medium AI: Basic strategy (win/block/center/corner/side).

    Args:
        board: Current board state (modified in place)
    """
    # Try to win
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = COMPUTER
                if check_winner(board, COMPUTER):
                    return
                board[i][j] = ' '

    # Try to block player
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = PLAYER
                if check_winner(board, PLAYER):
                    board[i][j] = COMPUTER
                    return
                board[i][j] = ' '

    # Take center if available
    if board[1][1] == ' ':
        board[1][1] = COMPUTER
        return

    # Take a random corner
    corners = [(0, 0), (0, BOARD_SIZE - 1),
               (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
    for i, j in corners:
        if board[i][j] == ' ':
            board[i][j] = COMPUTER
            return

    # Take a random side
    sides = [(0, 1), (1, 0), (1, BOARD_SIZE - 1),
             (BOARD_SIZE - 1, 1)]
    for i, j in sides:
        if board[i][j] == ' ':
            board[i][j] = COMPUTER
            return


def minimax(board, depth, maximizing_player):
    """
    Minimax algorithm for Tic-Tac-Toe.

    Args:
        board: Current board state
        depth: Current depth in search tree
        maximizing_player: True if computer (O), False if player (X)

    Returns:
        Best score (1 for win, -1 for loss, 0 for draw)
    """
    if check_winner(board, COMPUTER):
        return 1
    if check_winner(board, PLAYER):
        return -1
    if is_full(board):
        return 0

    if maximizing_player:
        max_score = -float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = COMPUTER
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_score = max(max_score, score)
        return max_score
    else:
        min_score = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = PLAYER
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_score = min(min_score, score)
        return min_score


def computer_move_hard(board):
    """Hard AI: Minimax algorithm for perfect play.

    Args:
        board: Current board state (modified in place)
    """
    best_score = -float('inf')
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = COMPUTER
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = COMPUTER


def get_difficulty_choice():
    """Get difficulty level from user input.

    Returns:
        Difficulty string ('easy', 'medium', or 'hard')
    """
    while True:
        choice = input("\nSelect difficulty:\n"
                       "1 - Easy (random moves)\n"
                       "2 - Medium (basic strategy)\n"
                       "3 - Hard (perfect play)\n"
                       "Enter your choice (1-3): ").lower()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def computer_move(board, difficulty):
    """
    Computer move dispatcher based on difficulty level.

    Args:
        board: The current board state (modified in place)
        difficulty: Difficulty level ('easy', 'medium', or 'hard')
    """
    if difficulty == '1' or difficulty == 'easy':
        computer_move_easy(board)
    elif difficulty == '2' or difficulty == 'medium':
        computer_move_medium(board)
    elif difficulty == '3' or difficulty == 'hard':
        computer_move_hard(board)
    else:
        # Default to easy if invalid
        computer_move_easy(board)