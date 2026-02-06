# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A simple command-line Tic-Tac-Toe game where the player plays against a basic AI computer. No external dependencies required.

## Running the Game

```bash
python3 tic_tac_toe.py
```

The game displays a numbered board (1-9) where players input moves by entering numbers.

## Code Architecture

Single-file script (`tic_tac_toe.py`) with clear functional separation:

- **Board display**: `print_board()` - Renders the 3x3 grid with ASCII borders
- **Game logic**: `check_winner()` - Checks all 8 possible winning lines (rows, columns, diagonals)
- **State checking**: `is_full()` - Determines if the board is full
- **AI opponent**: `computer_move()` - Makes decisions in priority order:
  1. Try to win immediately
  2. Block player from winning
  3. Take center if available
  4. Take a random corner
  5. Take a random side
- **Player input**: `get_player_move()` - Validates input and converts numbers 1-9 to (row, col) coordinates
- **Game loop**: `play_game()` - Manages the main game flow and play-again logic

## Key Implementation Details

- Board represented as a 3x3 list of lists: `board[row][col]`
- Player is 'X', Computer is 'O'
- Game ends when there's a winner or the board is full
- Handles keyboard interrupts gracefully