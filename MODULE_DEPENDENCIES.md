# Tic-Tac-Toe - Module Dependencies

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        main.py (Game Coordinator)                │
│                      play_game() function                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│  score_      │ │  board.py   │ │    ui.py     │
│  tracker.py  │ └──────┬──────┘ └──────────────┘
│              │         │
│ ┌────────────▼─────┐  │
│ │ constants.py     │  │
│ │ (SCORE_FILE,     │  │
│ │  Difficulty,     │  │
│ │  PLAYER,         │  │
│ │  COMPUTER)       │  │
│ └──────────────────┘  │
└───────────────────────┘
         │           │           │
         ▼           ▼           ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│  ai.py       │ │  input.py   │ │    (        │
│              │ │             │ │  (UI functions) │
│ ┌────────────▼─────┐ │ │ ┌────────▼─────┐ │
│ │ constants.py     │ │ │ │ constants.py │ │
│ │ (uses board.*)   │ │ │ │ (uses board.*)│ │
│ └──────────────────┘ │ │ └──────────────┘ │
│                      │ │                   │
│ ┌────────────────────▼─────┐ │ │ ┌────────────▼─────┐ │
│ │  board.py functions      │ │ │ │  board functions │ │
│ │  (check_winner,          │ │ │ │  (move_cursor,    │ │
│ │   is_full, get_...)      │ │ │ │   get_available_  │ │
│ │   make_move)             │ │ │ │   moves)          │ │
│ └──────────────────────────┘ │ │ └──────────────────┘ │
│                              │ │                     │
└──────────────────────────────┴───────────────────────┘
         │           │
         ▼           ▼
┌───────────────────────────────┐
│   board.py (Core Operations)  │
│                               │
│ ┌───────────────────────────┐ │
│ │ constants.py constants    │ │
│ │ (BOARD_SIZE)             │ │
│ └───────────────────────────┘ │
└───────────────────────────────┘
```

## 📦 Module Responsibilities

### Core Modules

1. **constants.py**
   - **Depends on**: None
   - **Used by**: All modules
   - **Provides**: Configuration values

2. **board.py**
   - **Depends on**: `constants.py`
   - **Used by**: `ai.py`, `input.py`, `main.py`
   - **Provides**: Board operations and utilities

3. **score_tracker.py**
   - **Depends on**: `constants.py`
   - **Used by**: `main.py`
   - **Provides**: Score management and persistence

4. **ui.py**
   - **Depends on**: `constants.py`
   - **Used by**: `main.py`
   - **Provides**: Display functions

### Game Logic Modules

5. **ai.py**
   - **Depends on**: `board.py` (check_winner, is_full, get_random_move)
   - **Used by**: `main.py`
   - **Provides**: AI opponent logic

6. **input.py**
   - **Depends on**: `board.py` (move_cursor, get_available_moves)
   - **Used by**: `main.py`
   - **Provides**: Player input handling

7. **main.py**
   - **Depends on**: All other modules
   - **Provides**: Game coordinator and main loop

## 🔄 Data Flow

```
User Action
    ↓
main.py (play_game)
    ↓
┌──────────────────────────────┐
│  Display menu / scores        │
│  Get difficulty selection     │
└────────────┬───────────────────┘
             │
             ▼
┌──────────────────────────────┐
│  Player move (input.py)       │
│  Computer move (ai.py)        │
│  Check win/draw (board.py)    │
└────────────┬───────────────────┘
             │
             ▼
┌──────────────────────────────┐
│  Update scores (score_tracker)│
│  Display result (ui.py)       │
│  Ask to play again            │
└──────────────────────────────┘
             │
             ▼
          Loop back
```

## 🎯 Key Dependencies

### Board Module Dependencies
- `constants.py` - For BOARD_SIZE, PLAYER, COMPUTER
- Internal functions use board state only

### AI Module Dependencies
- `board.check_winner()` - Win detection
- `board.is_full()` - Board full check
- `board.get_random_move()` - Easy AI move

### Input Module Dependencies
- `board.move_cursor()` - Arrow navigation
- `board.get_available_moves()` - Validation
- `constants.py` - Colors and formatting

### Score Tracker Dependencies
- `constants.py` - SCORE_FILE path
- Uses JSON for persistence

### UI Module Dependencies
- `constants.py` - Colors, formatting, player markers
- Displays game state

### Main Module Dependencies
- All other modules
- Coordinates game flow

## 🔗 Import Paths

```python
# From any location
from tic_tac_toe.constants import *
from tic_tac_toe.score_tracker import ScoreTracker
from tic_tac_toe.board import print_board, check_winner
from tic_tac_toe.ai import computer_move, minimax
from tic_tac_toe.input import get_player_move
from tic_tac_toe.ui import display_menu
from tic_tac_toe.main import play_game
```

## 📊 Complexity Analysis

- **Low**: `constants.py` (trivial)
- **Low-Medium**: `score_tracker.py`, `ui.py`, `board.py` (simple functions)
- **Medium**: `input.py`, `ai.py` (more complex logic)
- **Low**: `main.py` (coordination only)

## 🧪 Testing Strategy

- **Unit Tests**: Each module's functions
- **Integration Tests**: Module interaction
- **End-to-End**: Full game flow

## 📈 Extensibility

Easy to add:
- New difficulty levels (update `ai.py`)
- New board configurations (update `constants.py`)
- New display modes (update `ui.py`)
- New input methods (update `input.py`)

This modular structure makes the codebase flexible and maintainable.