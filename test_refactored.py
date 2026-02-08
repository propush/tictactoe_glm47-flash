#!/usr/bin/env python3
"""Test script to verify the refactored Tic-Tac-Toe code."""

import sys
import os
import tempfile

# Test imports
try:
    from tic_tac_toe.constants import SCORE_FILE, Difficulty, PLAYER, COMPUTER
    from tic_tac_toe.score_tracker import ScoreTracker
    from tic_tac_toe.board import print_board
    from tic_tac_toe.rules import TicTacToeRules
    from tic_tac_toe.ai_strategy import AIStrategyFactory, AIStrategy
    from tic_tac_toe.game_coordinator import TicTacToeGame
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
assert TicTacToeRules.check_winner(board, 'X')
print("✓ Win detection works")

# Test full board
board = [['X', 'O', 'X'],
         ['O', 'X', 'O'],
         ['O', 'X', 'X']]
assert TicTacToeRules.is_full(board)
print("✓ Full board detection works")

# Test available moves
board = [['X', ' ', 'O'],
         [' ', 'X', 'O'],
         ['O', ' ', ' ']]
moves = TicTacToeRules.get_available_moves(board)
assert len(moves) == 4
print("✓ Available moves function works")

# Test AI strategy factory
try:
    strategy = AIStrategyFactory.create(Difficulty.EASY)
    assert isinstance(strategy, AIStrategy)
    print("✓ AI Strategy Factory works")

    # Test easy AI move
    board = [[' ' for _ in range(3)] for _ in range(3)]
    move = strategy.get_move(board)
    assert move in TicTacToeRules.get_available_moves(board)
    print("✓ Easy AI strategy works")

    # Test medium AI move
    strategy = AIStrategyFactory.create(Difficulty.MEDIUM)
    move = strategy.get_move(board)
    assert move in TicTacToeRules.get_available_moves(board)
    print("✓ Medium AI strategy works")

    # Test hard AI move
    strategy = AIStrategyFactory.create(Difficulty.HARD)
    move = strategy.get_move(board)
    assert move in TicTacToeRules.get_available_moves(board)
    print("✓ Hard AI strategy works")

    # Ensure strategies do not mutate the board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    board[0][0] = 'X'
    snapshot = [row[:] for row in board]
    for difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
        strategy = AIStrategyFactory.create(difficulty)
        strategy.get_move(board)
        assert board == snapshot
    print("✓ AI strategies do not mutate board state")
except Exception as e:
    print(f"✗ AI Strategy tests failed: {e}")
    sys.exit(1)

# Test score tracker
from tic_tac_toe.score_tracker import InMemoryScoreStorage

tracker = ScoreTracker(storage=InMemoryScoreStorage())
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
print("✓ Score tracker works")

# Test game coordinator
try:
    from tic_tac_toe.score_tracker import InMemoryScoreStorage

    game = TicTacToeGame(score_tracker=ScoreTracker(storage=InMemoryScoreStorage()))
    assert game.score_tracker is not None
    print("✓ Game Coordinator can be instantiated")
except Exception as e:
    print(f"✗ Game Coordinator test failed: {e}")
    sys.exit(1)

# Test game loop ends immediately on computer win/draw
class FixedMoveStrategy:
    def __init__(self, move):
        self._move = move

    def get_move(self, board):
        return self._move


def assert_computer_turn_ends(board, move, expected_reason):
    game = TicTacToeGame(score_tracker=ScoreTracker(storage=InMemoryScoreStorage()))
    game.game_state.board = [row[:] for row in board]
    game.game_state.current_player = COMPUTER
    game.current_strategy = FixedMoveStrategy(move)

    turns = 0
    while True:
        result = game.play_turn()
        turns += 1
        if result and result['reason'] in ('win', 'draw'):
            assert result['reason'] == expected_reason
            break
        if turns > 1:
            raise AssertionError("Game did not end immediately after computer turn")

    assert turns == 1


# Computer win
board = [
    ['O', 'O', ' '],
    ['X', 'X', ' '],
    [' ', ' ', ' '],
]
assert_computer_turn_ends(board, (0, 2), 'win')
print("✓ Computer win ends game immediately")

# Computer draw
board = [
    ['X', 'O', 'X'],
    ['X', 'O', 'O'],
    ['O', 'X', ' '],
]
assert_computer_turn_ends(board, (2, 2), 'draw')
print("✓ Computer draw ends game immediately")

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)
