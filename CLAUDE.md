# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A terminal-based Tic-Tac-Toe game with multiple AI difficulty levels, arrow key navigation, and persistent score tracking. Built with Python and organized into modular packages.

## Running the Game

```bash
python3 tic_tac_toe/tic_tac_toe_game.py
# or
python3 -m tic_tac_toe.main
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

### Module Structure

The codebase is organized into modular packages in the `tic_tac_toe/` directory:

- **`constants.py`**: All configuration and constants (board size, player markers, ANSI colors, score file path, Difficulty enum)
- **`score_tracker.py`**: ScoreTracker class manages game statistics with persistent JSON storage
- **`board.py`**: Board operations and utilities
- **`ai.py`**: AI opponent logic and minimax algorithm
- **`input.py`**: Player input handling (both curses-based and fallback)
- **`ui.py`**: Terminal UI display functions
- **`main.py`**: Main game loop and coordination
- **`tic_tac_toe_game.py`**: Entry point for running the game

### Core Classes

- **`ScoreTracker`**: Manages game statistics with persistence across sessions via JSON file
- **`Difficulty`**: Enum class with EASY, MEDIUM, HARD constants

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

**AI Opponents**
- `computer_move_easy(board)`: Random valid moves
- `computer_move_medium(board)`: Win/block/center/corner/side priority
- `computer_move_hard(board)`: Minimax algorithm
- `computer_move(board, difficulty)`: Dispatcher based on difficulty level
- `get_difficulty_choice()`: Interactive difficulty selection menu

**Minimax Algorithm**
- `minimax(board, depth, maximizing_player)`: Recursive search algorithm for Hard AI
- Returns: 1 (win), -1 (loss), 0 (draw)
- Note: Implementation is simplified without alpha-beta pruning optimization

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
- `display_result(player_won, is_draw)`: Displays game outcome
- `display_scores(score_tracker)`: Shows session statistics
- `display_play_again_prompt()`: Asks user to play again

## Key Implementation Details

### Modular Architecture
- Code organized into separate modules with clear responsibilities
- Each module has specific import dependencies
- Main game loop coordinates between modules without direct dependencies
- Curses used only for arrow key input, main game uses standard terminal output

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
- **Easy**: Completely random valid moves
- **Medium**: Priority-based strategy (win > block > center > corner > side)
- **Hard**: Minimax algorithm for perfect play (unbeatable)
- Minimax returns: 1 (win), -1 (loss), 0 (draw)
- Implementation simplified without alpha-beta pruning optimization