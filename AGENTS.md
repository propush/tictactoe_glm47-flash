# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A terminal-based Tic-Tac-Toe game with multiple AI difficulty levels, arrow key navigation, and persistent score tracking. Built with Python following SOLID principles and Python design patterns.

## Running the Game

```bash
python3 run_game.py
# or
python3 -m tic_tac_toe.game_coordinator
```

## Game Features

### Input Methods
- **Arrow keys**: Navigate the board with visual cursor highlighting (via curses)
- **Enter**: Place your X at the cursor position
- **Keyboard interrupt (Ctrl+C)**: Cancel current move or quit game
- **'q'**: Quit move selection mode
- **Number input (fallback)**: Enter 1-9 if arrow keys fail (via curses)
- **Menu-driven difficulty selection**: Select difficulty via number input (1-3)

### Difficulty Levels
1. **Easy**: Completely random valid moves
2. **Medium**: Basic strategy (win/block/center/corner/side)
3. **Hard**: Minimax algorithm for perfect play (unbeatable)

### Score Tracking
- Persistent session statistics across multiple games
- Tracks: player wins, computer wins, draws, total games
- Displays at game start and game end

## Code Architecture

### Design Principles

This project demonstrates Python design patterns and SOLID principles:

- **Single Responsibility Principle**: Each class has one clear purpose
- **Separation of Concerns**: Clear boundaries between game state, rules, AI, and display
- **Composition Over Inheritance**: AI strategies composed rather than inherited
- **Rule of Three**: Wait before abstracting, kept simple with direct implementations

### Module Structure

The codebase is organized into focused, independent modules in the `tic_tac_toe/` directory:

**Core Modules**
- **`game_state.py`**: Manages current game state (board, current player, game status)
- **`rules.py`**: Game logic and rules (winner checks, move validation, win detection)
- **`ai_strategy.py`**: AI strategy patterns with abstraction and factory pattern
- **`game_coordinator.py`**: Orchestrates game flow and coordinates between layers

**Supporting Modules**
- **`constants.py`**: All configuration and constants (board size, player markers, colors, paths, Difficulty, GameResult)
- **`score_tracker.py`**: ScoreTracker class manages statistics with JSON persistence
- **`board.py`**: Board operations and utilities
- **`input.py`**: Player input handling (curses-based arrow keys and fallback)
- **`ui.py`**: Terminal display functions, user interface, and difficulty input

**Top-level Scripts**
- **`run_game.py`**: Convenience entry point

### Core Classes

**Game State & Rules**
- **`GameState`**: Manages current game state (board, current player, active status, winner)
- **`TicTacToeRules`**: Static methods for game logic (check_winner, is_full, make_move)

**AI Strategies**
- **`AIStrategy`**: Abstract base class for AI strategies
- **`RandomMoveStrategy`**: Easy AI: completely random valid moves
- **`MediumStrategy`**: Medium AI: priority-based strategy (win/block/center/corner/side)
- **`HardStrategy`**: Hard AI: Minimax algorithm with alpha-beta pruning
- **`AIStrategyFactory`**: Factory for creating strategy instances using Difficulty constants

**Constants**
- **`Difficulty`**: Difficulty level constants (EASY, MEDIUM, HARD)
- **`GameResult`**: Game outcome constants (PLAYER_WIN, COMPUTER_WIN, DRAW)

**Game Coordinator**
- **`TicTacToeGame`**: Main game class coordinating game flow and layer interactions

### Main Functions

**Input Handling**
- `get_arrow_move(stdscr, board)`: Arrow key-based move selection with curses
  - Shows visual cursor with green highlighting
  - Validates moves against occupied cells
  - Supports quit ('q') and cancel (Ctrl+C)

**Move Utilities**
- `move_cursor(cursor_row, cursor_col, direction, board)`: Navigate board with bounds checking
- `get_random_move(board)`: Returns random valid cell for Easy AI
- `get_available_moves(board)`: Returns list of empty cells
- `make_move(board, row, col, player)`: Places piece on board

**Minimax Algorithm**
- `minimax(board, depth, maximizing_player)`: Recursive search algorithm for Hard AI
- Implemented in `HardStrategy.get_move()`
- Returns: 1 (win), -1 (loss), 0 (draw)
- Includes alpha-beta pruning optimization

**Game Logic**
- `check_winner(board, player)`: Checks 8 possible winning lines (rows, columns, diagonals)
- `is_full(board)`: Determines if board is full
- `print_board(board, cursor_row, cursor_col)`: Renders board with optional cursor highlighting

**Game Flow**
- `play_game()`: Main loop managing:
  - Score display at game start/end
  - Difficulty selection
  - Alternating turns (X then O)
  - Win/draw detection
  - Play-again logic
- `get_player_move(board)`: Tries curses arrow keys first, falls back to number input
- `display_menu()`: Shows game introduction and controls
- `display_result(result)`: Displays game outcome using GameResult
- `display_scores(score_tracker)`: Shows session statistics
- `get_difficulty_input()`: Interactive difficulty selection menu (in ui.py)
- `display_play_again_prompt()`: Asks user to play again

## Key Implementation Details

### Architecture Design

**Separation of Concerns**
```
┌─────────────────────────────────────────────────────────────────┐
│  Game Coordinator Layer (game_coordinator.py)                   │
│  - TicTacToeGame: Orchestrates game flow                      │
│  - Coordinates between all layers                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  AI Strategy Layer (ai_strategy.py)                            │
│  - AIStrategy: Abstract base class                             │
│  - Concrete strategies: RandomMoveStrategy, MediumStrategy,     │
│    HardStrategy                                               │
│  - AIStrategyFactory: Factory pattern for strategy creation    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Rules Layer (rules.py)                                         │
│  - TicTacToeRules: Game logic and rules                        │
│  - Static methods: check_winner, is_full, make_move            │
│  - Pure functions for reusability                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  State Layer (game_state.py)                                    │
│  - GameState: Current game state management                    │
│  - Board, current player, game status                          │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles Applied

**Single Responsibility Principle**
- `GameState`: Manages game state only
- `TicTacToeRules`: Contains all game logic only
- `TicTacToeGame`: Coordinates game flow only
- `AIStrategy`: Abstract behavior, concrete implementations handle specific strategies
- `ScoreTracker`: Tracks scores only (display handled by ui.py)

**Composition Over Inheritance**
- AI strategies composed using abstract base class
- Factory creates strategy instances based on Difficulty constants
- No rigid inheritance hierarchies

**KISS (Keep It Simple)**
- Direct implementations rather than premature abstraction
- Simple factory pattern for strategy creation
- Clear, focused functions without over-engineering

**Separation of Concerns**
- Clear boundaries between layers
- Each layer depends only on layers below it
- No circular dependencies between modules
- UI input (get_difficulty_input) lives in ui.py, not in factory
- AI strategies work on board copies, never mutate the game board

### Terminal UI
- Uses `curses` library for arrow key navigation and cursor highlighting
- ANSI color codes (RED, GREEN, BOLD, RESET constants) for visual feedback
- Color pairs: White (normal), Green (highlighted), Red (errors)
- Terminal output via standard `print()` statements

### Board Representation
- 3x3 list of lists: `board[row][col]`
- Cells contain: `' '` (empty), `'X'` (player), `'O'` (computer)

### Game Flow
- Player is 'X', Computer is 'O'
- Game ends when winner found or board is full
- Alternating turns with clear turn indicators
- Play-again prompt at game end

### Persistence
- Scores stored in JSON file: `tic_tac_toe_scores.json`
- Auto-saved after each game completion
- Loads existing scores on game initialization
- Tracks session statistics across multiple game sessions

### AI Implementation
- **Easy**: RandomMoveStrategy makes completely random valid moves
- **Medium**: MediumStrategy uses priority-based strategy (win > block > center > corner > side)
- **Hard**: HardStrategy uses Minimax algorithm with alpha-beta pruning for perfect play
- AI strategies use `copy.deepcopy(board)` to avoid mutating the game board
- Minimax returns: 1 (win), -1 (loss), 0 (draw)
- Implementation includes alpha-beta pruning optimization

### Pattern Implementations

**Factory Pattern (AIStrategyFactory)**
```python
# Create strategy based on Difficulty constant
strategy = AIStrategyFactory.create(Difficulty.HARD)
move = strategy.get_move(board)
```

**GameResult Enum**
```python
# Clear game outcomes instead of ambiguous booleans
score_tracker.record_result(GameResult.PLAYER_WIN)
display_result(GameResult.DRAW)
```

**Abstract Base Class (AIStrategy)**
```python
# Base class for AI strategies
class AIStrategy(ABC):
    @abstractmethod
    def get_move(self, board):
        pass
```

**Dependency Injection**
```python
# Game coordinator accepts score tracker as dependency
class TicTacToeGame:
    def __init__(self, score_tracker):
        self.score_tracker = score_tracker
```

**Static Methods for Pure Logic**
- `TicTacToeRules` methods are static to ensure stateless, pure functions
- Easy to test and reuse across different contexts

### Testing Strategy
- Each layer can be tested independently
- GameState can be tested with mocked dependencies
- Rules can be tested with board state alone
- Strategies can be tested with board states (they don't mutate the board)
- Mock dependencies allow isolation of each component
- `InMemoryScoreStorage` provided for testing score tracking

### Backward Compatibility
- No legacy entry points are maintained.
- New code should use `tic_tac_toe/game_coordinator.py` or `run_game.py`.
