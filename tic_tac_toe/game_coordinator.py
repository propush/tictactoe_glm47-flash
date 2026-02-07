"""Game coordinator for Tic-Tac-Toe.

Coordinates between game state, rules, AI, and display layers.
Uses Separation of Concerns principle.
"""

import sys
from .game_state import GameState
from .rules import TicTacToeRules
from .ai_strategy import AIStrategyFactory
from .ui import display_menu, display_result, display_scores, display_play_again_prompt
from .score_tracker import ScoreTracker
from .constants import PLAYER, COMPUTER


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
            difficulty: Difficulty level ('easy', 'medium', 'hard') or number (1-3)
        """
        self.current_strategy = AIStrategyFactory.create(difficulty)

    def get_player_move(self):
        """Get player move from input.

        Returns:
            Tuple of (row, col) or None if cancelled
        """
        from .input import get_player_move
        return get_player_move(self.game_state.board)

    def get_computer_move(self):
        """Get computer move from AI.

        Returns:
            Tuple of (row, col) or None if no moves available
        """
        if self.current_strategy:
            move = self.current_strategy.get_move(self.game_state.board)
            if move:
                self.game_state.board[move[0]][move[1]] = self.game_state.get_player_marker()
            return move
        return None

    def play_turn(self):
        """Play one turn of the game."""
        if self.game_state.is_player_turn():
            return self._player_turn()
        else:
            return self._computer_turn()

    def _player_turn(self):
        """Handle player's turn."""
        move = self.get_player_move()
        if move is None:
            return None

        row, col = move
        TicTacToeRules.make_move(self.game_state.board, row, col, PLAYER)

        # Check win/draw
        player_won = TicTacToeRules.check_winner(self.game_state.board, PLAYER)
        if player_won:
            return {'winner': 'player', 'reason': 'win'}
        if TicTacToeRules.is_full(self.game_state.board):
            return {'winner': None, 'reason': 'draw'}

        self.game_state.switch_player()
        return {'winner': None, 'reason': 'continue'}

    def _computer_turn(self):
        """Handle computer's turn."""
        move = self.get_computer_move()
        if move is None:
            return None

        computer_won = TicTacToeRules.check_winner(self.game_state.board, COMPUTER)
        if computer_won:
            return {'winner': 'computer', 'reason': 'win'}
        if TicTacToeRules.is_full(self.game_state.board):
            return {'winner': None, 'reason': 'draw'}

        self.game_state.switch_player()
        return {'winner': None, 'reason': 'continue'}

    def check_game_over(self):
        """Check if the game has ended.

        Returns:
            Result dictionary or None if game continues
        """
        player_won = TicTacToeRules.check_winner(self.game_state.board, PLAYER)
        computer_won = TicTacToeRules.check_winner(self.game_state.board, COMPUTER)

        result = TicTacToeRules.check_game_over(
            self.game_state.board, player_won, computer_won
        )

        if result['game_over']:
            self.game_state.game_over_reason = result['reason']
            return result

        return None

    def display_board(self):
        """Display the current board state."""
        from .board import print_board
        print_board(self.game_state.board)

    def display_result(self):
        """Display the game result."""
        display_result(self.game_state.game_over_reason == 'draw',
                      self.game_state.game_over_reason == 'win' and
                      self.game_state.game_over_reason == 'player')


def play_game():
    """Main game loop."""
    score_tracker = ScoreTracker()

    while True:
        display_scores(score_tracker)
        display_menu()

        # Difficulty selection
        difficulty = AIStrategyFactory.get_difficulty_input()

        # Create and initialize game
        game = TicTacToeGame(score_tracker)
        game.set_difficulty(difficulty)
        game.start_new_game()

        # Play the game
        while True:
            game.display_board()

            result = game.play_turn()
            if result is None:
                continue  # Cancelled move

            if result['reason'] in ('win', 'draw'):
                break

            game.display_board()
            result = game.play_turn()

        # Check if game is actually over
        game_result = game.check_game_over()
        if not game_result:
            continue

        # Record result
        player_won = game_result['winner'] == 'player'
        is_draw = game_result['reason'] == 'draw'
        score_tracker.record_win(player_won, is_draw)

        # Display result
        game.display_result()

        # Play again?
        if not display_play_again_prompt():
            break


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)