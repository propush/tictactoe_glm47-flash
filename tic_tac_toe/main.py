"""Main game loop and coordination for Tic-Tac-Toe game."""

import sys
from .score_tracker import ScoreTracker
from .board import print_board, check_winner, is_full, get_available_moves, make_move
from .ai import computer_move, get_difficulty_choice
from .input import get_player_move
from .ui import display_menu, display_result, display_scores, display_play_again_prompt


def play_game():
    """Main game loop."""
    # Initialize score tracker
    score_tracker = ScoreTracker()

    while True:
        # Display current scores at the start of each game
        display_scores(score_tracker)

        display_menu()

        # Difficulty selection
        difficulty = get_difficulty_choice()

        player_won = False
        # Initialize game state
        board = [[' ' for _ in range(3)] for _ in range(3)]
        player = 'X'
        computer = 'O'
        game_over = False

        while not game_over:
            print_board(board)

            if player == 'X':
                row, col = get_player_move(board)
                make_move(board, row, col, player)
                print(f"\nYou placed {player} at position {row * 3 + col + 1}")

                if check_winner(board, player):
                    print_board(board)
                    print("🎉 Congratulations! You win!")
                    player_won = True
                    game_over = True
                elif is_full(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                    player_won = None
                else:
                    player = 'O'
            else:
                print("\nComputer is thinking...")
                computer_move(board, difficulty)
                print(f"Computer placed {computer}")

                if check_winner(board, computer):
                    print_board(board)
                    print("😔 Computer wins!")
                    game_over = True
                    player_won = False
                elif is_full(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                    player_won = None
                else:
                    player = 'X'

        # Record the result
        score_tracker.record_win(player_won, player_won is None)

        # Display result
        display_result(player_won, player_won is None)

        # Play again?
        if not display_play_again_prompt():
            break


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)