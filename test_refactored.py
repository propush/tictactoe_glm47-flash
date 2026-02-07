#!/usr/bin/env python3
"""Test script to verify the refactored Tic-Tac-Toe code."""

import sys
import os
import tempfile

# Test imports
try:
    from tic_tac_toe.constants import SCORE_FILE, Difficulty, PLAYER, COMPUTER
    from tic_tac_toe.score_tracker import ScoreTracker
    from tic_tac_toe.board import print_board, check_winner, is_full, get_available_moves
    from tic_tac_toe.ai import computer_move, get_difficulty_choice
    from tic_tac_toe.input import get_player_move
    from tic_tac_toe.ui import display_menu, display_result, display_scores
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test constants
assert SCORE_FILE == "tic_tac_toe_scores.json"
assert Difficulty.EASY == "easy"
assert Difficulty.MEDIUM == "medium"
assert Difficulty.HARD == "hard"
assert PLAYER == 'X'
assert COMPUTER == 'O'
print("✓ Constants are correct")

# Test board
board = [[' ' for _ in range(3)] for _ in range(3)]
print_board(board)
print("✓ Board display works")

# Test win detection
board[0] = ['X', 'X', 'X']
assert check_winner(board, 'X')
print("✓ Win detection works")

# Test full board
board = [['X', 'O', 'X'],
         ['O', 'X', 'O'],
         ['O', 'X', 'X']]
assert is_full(board)
print("✓ Full board detection works")

# Test available moves
board = [['X', ' ', 'O'],
         [' ', 'X', 'O'],
         ['O', ' ', ' ']]
moves = get_available_moves(board)
assert len(moves) == 4
print("✓ Available moves function works")

# Test score tracker
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
    temp_file = f.name

tracker = ScoreTracker(score_file=temp_file)
assert tracker.player_wins == 0
assert tracker.computer_wins == 0
assert tracker.draws == 0
assert tracker.total_games == 0
tracker.record_win(True, False)
assert tracker.player_wins == 1
tracker.record_win(False, False)
assert tracker.computer_wins == 1
tracker.record_win(None, True)
assert tracker.draws == 1
assert tracker.total_games == 3
os.unlink(temp_file)
print("✓ Score tracker works")

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)