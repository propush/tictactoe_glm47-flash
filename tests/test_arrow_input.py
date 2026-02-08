import pytest

from tic_tac_toe.constants import PLAYER, COMPUTER, GameResult
from tic_tac_toe.game_coordinator import TicTacToeGame
from tic_tac_toe.input import get_arrow_move
from tic_tac_toe.score_tracker import ScoreTracker, InMemoryScoreStorage


class FakeWindow:
    def __init__(self, key_queue):
        self._key_queue = list(key_queue)

    def getch(self):
        if not self._key_queue:
            raise AssertionError("Test key queue exhausted")
        key = self._key_queue.pop(0)
        if key == "KEYBOARD_INTERRUPT":
            raise KeyboardInterrupt
        return key

    def addstr(self, *args, **kwargs):
        return None

    def clear(self):
        return None

    def refresh(self):
        return None

    def nodelay(self, _):
        return None

    def keypad(self, _):
        return None


class FakeCurses:
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_LEFT = 260
    KEY_RIGHT = 261
    KEY_ENTER = 343

    COLOR_WHITE = 0
    COLOR_BLACK = 0
    COLOR_GREEN = 2
    COLOR_RED = 1

    A_BOLD = 1

    def __init__(self, key_queue):
        self._key_queue = key_queue

    def initscr(self):
        return FakeWindow(self._key_queue)

    def endwin(self):
        return None

    def start_color(self):
        return None

    def use_default_colors(self):
        return None

    def init_pair(self, *_args):
        return None

    def color_pair(self, _):
        return 0


def make_game(board=None):
    game = TicTacToeGame(score_tracker=ScoreTracker(storage=InMemoryScoreStorage()))
    if board is not None:
        game.game_state.board = [row[:] for row in board]
    game.game_state.current_player = PLAYER
    return game


def patch_curses(monkeypatch, key_queue):
    fake_curses = FakeCurses(key_queue)
    import tic_tac_toe.input as input_module
    monkeypatch.setattr(input_module, "curses", fake_curses)
    monkeypatch.setattr(input_module.time, "sleep", lambda _seconds: None)


def test_arrow_move_places_x(monkeypatch):
    key_queue = [
        FakeCurses.KEY_RIGHT,
        FakeCurses.KEY_DOWN,
        ord("\n"),
    ]
    patch_curses(monkeypatch, key_queue)

    game = make_game()
    result = game.play_turn()

    assert game.game_state.board[1][1] == PLAYER
    assert result is not None
    assert result["reason"] == "continue"


def test_invalid_occupied_cell_then_valid_move(monkeypatch):
    board = [[" "] * 3 for _ in range(3)]
    board[0][0] = PLAYER

    key_queue = [
        ord("\n"),
        FakeCurses.KEY_RIGHT,
        ord("\n"),
    ]
    patch_curses(monkeypatch, key_queue)

    game = make_game(board)
    result = game.play_turn()

    assert game.game_state.board[0][1] == PLAYER
    assert result is not None
    assert result["reason"] == "continue"


def test_quit_returns_none(monkeypatch):
    key_queue = [ord("q")]
    patch_curses(monkeypatch, key_queue)
    stdscr = FakeWindow(key_queue)
    board = [[" "] * 3 for _ in range(3)]
    result = get_arrow_move(stdscr, board)

    assert result is None


def test_keyboard_interrupt_returns_none(monkeypatch):
    key_queue = ["KEYBOARD_INTERRUPT"]
    patch_curses(monkeypatch, key_queue)
    stdscr = FakeWindow(key_queue)
    board = [[" "] * 3 for _ in range(3)]
    result = get_arrow_move(stdscr, board)

    assert result is None


def test_win_via_arrow_move(monkeypatch):
    board = [
        [PLAYER, PLAYER, " "],
        [COMPUTER, COMPUTER, " "],
        [" ", " ", " "],
    ]

    key_queue = [
        FakeCurses.KEY_RIGHT,
        FakeCurses.KEY_RIGHT,
        ord("\n"),
    ]
    patch_curses(monkeypatch, key_queue)

    game = make_game(board)
    result = game.play_turn()

    assert result is not None
    assert result["reason"] == "win"
    assert result["result"] == GameResult.PLAYER_WIN
    assert game.game_state.winner == "player"


def test_draw_via_arrow_move(monkeypatch):
    board = [
        [PLAYER, COMPUTER, PLAYER],
        [PLAYER, COMPUTER, COMPUTER],
        [COMPUTER, PLAYER, " "],
    ]

    key_queue = [
        FakeCurses.KEY_DOWN,
        FakeCurses.KEY_DOWN,
        FakeCurses.KEY_RIGHT,
        FakeCurses.KEY_RIGHT,
        ord("\n"),
    ]
    patch_curses(monkeypatch, key_queue)

    game = make_game(board)
    result = game.play_turn()

    assert result is not None
    assert result["reason"] == "draw"
    assert result["result"] == GameResult.DRAW
