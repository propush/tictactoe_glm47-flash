# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A terminal-based Tic-Tac-Toe game with multiple AI difficulty levels, arrow key navigation, and persistent score tracking. Built with Python's `curses` library for terminal UI.

## Running the Game

```bash
python3 tic_tac_toe.py
```

## Game Features

### Input Methods
- **Arrow keys**: Navigate the board with visual cursor highlighting
- **Enter**: Place your X at the cursor position
- **Keyboard interrupt (Ctrl+C)**: Cancel current move or quit game
- **'q'**: Quit move selection mode
- **Number input (fallback)**: Enter 1-9 if arrow keys fail

### Difficulty Levels
1. **Easy**: Completely random valid moves
2. **Medium**: Basic strategy (win/block/center/corner/side)
3. **Hard**: Minimax algorithm for perfect play (unbeatable)

### Score Tracking
- Persistent session statistics across multiple games
- Tracks: player wins, computer wins, draws, total games
- Displays at game start and game end

## Code Architecture

### Core Classes
- **`ScoreTracker`**: Manages game statistics with persistence across sessions
- **`Difficulty`**: Enum for AI difficulty levels

### Main Functions

**Input Handling**
- `get_arrow_move(stdscr, board)`: Arrow key-based move selection with curses
  - Shows visual cursor with green highlighting
  - Validates moves against occupied cells
  - Supports quit ('q') and cancel (Ctrl+C)

**Move Utilities**
- `move_cursor(cursor_row, cursor_col, direction, board)`: Navigate board with bounds checking
- `get_random_move(board)`: Returns random valid cell for Easy AI

**AI Opponents**
- `computer_move_easy(board)`: Random valid moves
- `computer_move_medium(board)`: Win/block/center/corner/side priority
- `computer_move_hard(board)`: Minimax algorithm
- `computer_move(board, difficulty)`: Dispatcher based on difficulty level

**Minimax Algorithm**
- `minimax(board, depth, maximizing_player)`: Recursive search with alpha-beta pruning
- Returns: 1 (win), -1 (loss), 0 (draw)

**Game Logic**
- `check_winner(board, player)`: Checks 8 possible winning lines
- `is_full(board)`: Determines if board is full
- `print_board(board, cursor_row, cursor_col)`: Renders board with optional cursor highlighting

**Game Flow**
- `play_game()`: Main loop managing:
  - Score display at game start/end
  - Difficulty selection
  - Alternating turns (X then O)
  - Win/draw detection
  - Play-again logic
- `get_player_move(board)`: Tries arrow keys first, falls back to number input

## Key Implementation Details

- **Terminal UI**: Uses `curses` library for color-coded display and cursor navigation
- **Color pairs**: White (normal), Green (highlighted), Red (errors)
- **Board representation**: 3x3 list of lists: `board[row][col]`
- **Player is 'X', Computer is 'O'**
- **Game ends** when winner found or board is full
- **Persistent scores**: Stored in memory across multiple game sessions
- **Keyboard interrupts**: Gracefully handled with exit message