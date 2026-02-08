"""Game coordinator for Tic-Tac-Toe.

Coordinates between game state, rules, AI, and display layers.
Uses Separation of Concerns principle.
"""

import sys
from .game_state import GameState
from .rules import TicTacToeRules
from .ai_strategy import AIStrategyFactory
from .input import get_player_move
from .board import print_board
from .ui import (display_menu, display_result, display_scores,
                 display_play_again_prompt, get_difficulty_input)
from .score_tracker import ScoreTracker
from .constants import PLAYER, COMPUTER, GameResult


class TicTacToeGame:
    """Main game class that coordinates game flow."""

    def __init__(self, score_tracker):
        """Initialize game with score tracker.

        Args:
            score_tracker: ScoreTracker instance
        """
        self.score_tracker = score_tracker
        self.game_state = GameState()
        self.current_strategy = None

    def start_new_game(self):
        """Start a new game."""
        self.game_state.reset()

    def set_difficulty(self, difficulty):
        """Set AI difficulty.

        Args:
            difficulty: Difficulty constant (Difficulty.EASY, MEDIUM, or HARD)
        """
        self.current_strategy = AIStrategyFactory.create(difficulty)

    def play_turn(self):
        """Play one turn of the game.

        Returns:
            Legacy result dictionary with `reason` key, or None if move cancelled.
        """
        if self.game_state.is_player_turn():
            move = get_player_move(self.game_state.board, last_move=self.game_state.last_move)
            marker = PLAYER
        else:
            move = self.current_strategy.get_move(self.game_state.board) if self.current_strategy else None
            marker = COMPUTER

        if move is None:
            return None

        row, col = move
        if not TicTacToeRules.make_move(self.game_state.board, row, col, marker):
            return None
        self.game_state.last_move = (row, col)

        winning_line = TicTacToeRules.get_winning_line(self.game_state.board, marker)
        if winning_line:
            result = GameResult.PLAYER_WIN if marker == PLAYER else GameResult.COMPUTER_WIN
            self.game_state.winner = 'player' if marker == PLAYER else 'computer'
            self.game_state.game_over_reason = 'win'
            self.game_state.winning_line = winning_line
            return {'reason': 'win', 'result': result}
        if TicTacToeRules.is_full(self.game_state.board):
            self.game_state.game_over_reason = 'draw'
            return {'reason': 'draw', 'result': GameResult.DRAW}

        self.game_state.switch_player()
        return {'reason': 'continue', 'result': None}

    def display_board(self):
        """Display the current board state."""
        print_board(
            self.game_state.board,
            last_move=self.game_state.last_move,
            winning_line=self.game_state.winning_line,
            show_labels=True,
        )


def play_game():
    """Main game loop."""
    score_tracker = ScoreTracker()

    # Show stats at program start
    display_scores(score_tracker)

    while True:
        display_menu()

        # Difficulty selection
        difficulty = get_difficulty_input()

        # Create and initialize game
        game = TicTacToeGame(score_tracker)
        game.set_difficulty(difficulty)
        game.start_new_game()

        # Play the game
        result = None
        while True:
            game.display_board()
            result = game.play_turn()
            if result and result.get('reason') in ('win', 'draw'):
                break

        # Show final board state (including winning line) before result.
        game.display_board()

        # Record and display result
        game_result = result['result']
        score_tracker.record_result(game_result)
        display_result(game_result)
        display_scores(score_tracker)

        # Play again?
        if not display_play_again_prompt():
            break


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
