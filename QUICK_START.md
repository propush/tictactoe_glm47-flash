# Tic-Tac-Toe - Quick Start Guide

## 🎮 How to Play

Run the game:
```bash
python3 tic_tac_toe_game.py
```

## 🕹️ Controls

- **Arrow Keys**: Move the cursor
- **Enter**: Place your X
- **Ctrl+C**: Cancel move or quit game
- **'q'**: Quit move selection mode
- **Number Input (1-9)**: Fallback method if arrow keys fail

## 🤖 Difficulty Levels

1. **Easy** - Computer makes random moves
2. **Medium** - Computer uses basic strategy (blocks you, takes center)
3. **Hard** - Computer uses perfect play (minimax algorithm)

## 📊 Scores

Scores are automatically saved to `tic_tac_toe_scores.json` and persist across game sessions.

## 🧪 Running Tests

Test the refactored code:
```bash
python3 test_refactored.py
```

## 📦 Package Structure

```python
# Import modules
from tic_tac_toe.constants import Difficulty, PLAYER, COMPUTER
from tic_tac_toe.score_tracker import ScoreTracker
from tic_tac_toe.board import check_winner, is_full
from tic_tac_toe.ai import minimax, computer_move
from tic_tac_toe.input import get_player_move
from tic_tac_toe.ui import display_menu
from tic_tac_toe.main import play_game

# Run game
play_game()
```

## 📖 Documentation

- `REFACTORING.md` - Detailed refactoring documentation
- `REFACTORING_SUMMARY.md` - Complete summary of changes
- Module docstrings - Each module includes detailed documentation

## ✨ Features

- ✅ Terminal-based game
- ✅ Arrow key navigation with cursor
- ✅ Three AI difficulty levels
- ✅ Persistent score tracking
- ✅ Win/draw detection
- ✅ Play-again functionality
- ✅ Color-coded display
- ✅ Fallback number input
- ✅ Keyboard interrupt handling

## 🔧 Development

The codebase is modular and well-organized:
- **constants.py** - Configuration
- **score_tracker.py** - Score management
- **board.py** - Board operations
- **ai.py** - AI logic
- **input.py** - Player input
- **ui.py** - Display functions
- **main.py** - Game coordinator

## 🚀 Next Steps

Try the game, then explore the codebase to understand the refactored structure!

---

For detailed information, see `REFACTORING.md` and `REFACTORING_SUMMARY.md`.