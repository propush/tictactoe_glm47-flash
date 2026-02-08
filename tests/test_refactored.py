import pytest

from tic_tac_toe.ai_strategy import AIStrategy, AIStrategyFactory
from tic_tac_toe.board import print_board
from tic_tac_toe.constants import COMPUTER, PLAYER, Difficulty, SCORE_FILE
from tic_tac_toe.game_coordinator import TicTacToeGame
from tic_tac_toe.rules import TicTacToeRules
from tic_tac_toe.score_tracker import InMemoryScoreStorage, ScoreTracker


def test_constants():
    assert SCORE_FILE == "tic_tac_toe_scores.json"
    assert Difficulty.EASY == "easy"
    assert Difficulty.MEDIUM == "medium"
    assert Difficulty.HARD == "hard"
    assert PLAYER == "X"
    assert COMPUTER == "O"


def test_board_display():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print_board(board)


def test_win_detection():
    board = [[" " for _ in range(3)] for _ in range(3)]
    board[0] = ["X", "X", "X"]
    assert TicTacToeRules.check_winner(board, "X")


def test_full_board():
    board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", "X"],
    ]
    assert TicTacToeRules.is_full(board)


def test_available_moves():
    board = [
        ["X", " ", "O"],
        [" ", "X", "O"],
        ["O", " ", " "],
    ]
    moves = TicTacToeRules.get_available_moves(board)
    assert len(moves) == 4


def test_ai_strategy_factory_and_moves():
    strategy = AIStrategyFactory.create(Difficulty.EASY)
    assert isinstance(strategy, AIStrategy)

    board = [[" " for _ in range(3)] for _ in range(3)]
    move = strategy.get_move(board)
    assert move in TicTacToeRules.get_available_moves(board)

    strategy = AIStrategyFactory.create(Difficulty.MEDIUM)
    move = strategy.get_move(board)
    assert move in TicTacToeRules.get_available_moves(board)

    strategy = AIStrategyFactory.create(Difficulty.HARD)
    move = strategy.get_move(board)
    assert move in TicTacToeRules.get_available_moves(board)


def test_ai_strategies_do_not_mutate_board():
    board = [[" " for _ in range(3)] for _ in range(3)]
    board[0][0] = "X"
    snapshot = [row[:] for row in board]
    for difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
        strategy = AIStrategyFactory.create(difficulty)
        strategy.get_move(board)
        assert board == snapshot


def test_score_tracker_in_memory():
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


def test_game_coordinator_instantiation():
    game = TicTacToeGame(score_tracker=ScoreTracker(storage=InMemoryScoreStorage()))
    assert game.score_tracker is not None


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
        if result and result["reason"] in ("win", "draw"):
            assert result["reason"] == expected_reason
            break
        if turns > 1:
            raise AssertionError("Game did not end immediately after computer turn")

    assert turns == 1


def test_computer_turn_end_win():
    board = [
        ["O", "O", " "],
        ["X", "X", " "],
        [" ", " ", " "],
    ]
    assert_computer_turn_ends(board, (0, 2), "win")


def test_computer_turn_end_draw():
    board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", " "],
    ]
    assert_computer_turn_ends(board, (2, 2), "draw")
