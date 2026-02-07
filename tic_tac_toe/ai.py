"""AI opponent logic and minimax algorithm for Tic-Tac-Toe game.

Note: This module is kept for backward compatibility.
Please use ai_strategy.AIStrategyFactory for new code.
"""

import random
from .ai_strategy import AIStrategyFactory


# Legacy functions kept for backward compatibility
def computer_move_easy(board):
    """Easy AI: Makes completely random valid moves.

    Args:
        board: Current board state (modified in place)
    """
    strategy = AIStrategyFactory.create('easy')
    move = strategy.get_move(board)
    if move:
        board[move[0]][move[1]] = 'O'


def computer_move_medium(board):
    """Medium AI: Basic strategy (win/block/center/corner/side).

    Args:
        board: Current board state (modified in place)
    """
    strategy = AIStrategyFactory.create('medium')
    move = strategy.get_move(board)
    if move:
        board[move[0]][move[1]] = 'O'


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
    from .rules import check_winner, is_full

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
    """Hard AI: Minimax algorithm for perfect play.

    Args:
        board: Current board state (modified in place)
    """
    strategy = AIStrategyFactory.create('hard')
    move = strategy.get_move(board)
    if move:
        board[move[0]][move[1]] = 'O'


def get_difficulty_choice():
    """Get difficulty level from user input.

    Returns:
        Difficulty string ('easy', 'medium', or 'hard')
    """
    return AIStrategyFactory.get_difficulty_input()


def computer_move(board, difficulty):
    """
    Computer move dispatcher based on difficulty level.

    Args:
        board: The current board state (modified in place)
        difficulty: Difficulty level ('easy', 'medium', or 'hard')
    """
    strategy = AIStrategyFactory.create(difficulty)
    move = strategy.get_move(board)
    if move:
        board[move[0]][move[1]] = 'O'