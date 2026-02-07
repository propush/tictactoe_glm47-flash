"""Score management and persistence for Tic-Tac-Toe game.

Implements dependency injection for score storage to enable testing.
"""

import json
from abc import ABC, abstractmethod
from .constants import SCORE_FILE


class ScoreStorage(ABC):
    """Abstract base class for score storage."""

    @abstractmethod
    def load(self):
        """Load scores from storage.

        Returns:
            Dictionary with score data
        """
        pass

    @abstractmethod
    def save(self, data):
        """Save scores to storage.

        Args:
            data: Dictionary with score data
        """
        pass


class JsonFileScoreStorage(ScoreStorage):
    """JSON file-based score storage."""

    def __init__(self, file_path=None):
        """Initialize with optional file path.

        Args:
            file_path: Path to JSON file, defaults to SCORE_FILE
        """
        self.file_path = file_path or SCORE_FILE

    def load(self):
        """Load scores from JSON file."""
        import os
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            'player_wins': 0,
            'computer_wins': 0,
            'draws': 0,
            'total_games': 0
        }

    def save(self, data):
        """Save scores to JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            raise IOError(f"Could not save scores to file: {e}")


class InMemoryScoreStorage(ScoreStorage):
    """In-memory score storage for testing purposes."""

    def __init__(self):
        """Initialize with empty storage."""
        self._data = {
            'player_wins': 0,
            'computer_wins': 0,
            'draws': 0,
            'total_games': 0
        }

    def load(self):
        """Return current in-memory scores."""
        return self._data.copy()

    def save(self, data):
        """Update in-memory scores."""
        self._data.update(data)


class ScoreTracker:
    """Track game scores across multiple sessions with persistent storage."""

    def __init__(self, storage=None):
        """Initialize score tracker with optional storage.

        Args:
            storage: ScoreStorage instance for dependency injection. Defaults to JsonFileScoreStorage.
        """
        self.storage = storage or JsonFileScoreStorage()
        self._scores = self.storage.load()

    def record_win(self, player_won, is_draw):
        """Record a win/loss/draw result.

        Args:
            player_won: True if player won
            is_draw: True if game ended in a draw
        """
        self._scores['total_games'] += 1
        if player_won:
            self._scores['player_wins'] += 1
        elif is_draw:
            self._scores['draws'] += 1
        else:
            self._scores['computer_wins'] += 1
        self.storage.save(self._scores)

    @property
    def player_wins(self):
        """Get player wins count."""
        return self._scores['player_wins']

    @property
    def computer_wins(self):
        """Get computer wins count."""
        return self._scores['computer_wins']

    @property
    def draws(self):
        """Get draws count."""
        return self._scores['draws']

    @property
    def total_games(self):
        """Get total games count."""
        return self._scores['total_games']

    def display_scores(self):
        """Display current session statistics."""
        import sys
        sys.stdout.write("\n" + "=" * 30 + "\n")
        sys.stdout.write("📊 SESSION STATISTICS\n")
        sys.stdout.write("=" * 30 + "\n")
        sys.stdout.write(f"Player wins:      {self.player_wins}\n")
        sys.stdout.write(f"Computer wins:    {self.computer_wins}\n")
        sys.stdout.write(f"Draws:            {self.draws}\n")
        sys.stdout.write(f"Total games:      {self.total_games}\n")
        sys.stdout.write("=" * 30 + "\n")
        sys.stdout.flush()