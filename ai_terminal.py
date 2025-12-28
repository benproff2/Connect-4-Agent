import math
from game_logic import *


def minimax(board, depth, alpha, beta, maximizing_player):
    """Recursively evaluate the game states using the MiniMax algorithm with Alpha-Beta pruning

    Args:
        board: The current game board
        depth: The remaining depth to search
        alpha: The alpha value for pruning
        beta: The beta value for pruning
        maximizing_player: True if it's the maximizing player's turn, False for minimizing
    
    Returns:
        The evaluated score of the best move from this position
    """
    if depth == 0 or check_win(board, 1) or check_win(board, 2) or is_draw(board):
        # Evaluate the board from Player 1’s perspective (for example)
        return heuristic(board, 1)

    if maximizing_player:
        # Player 1's turn (maximize score)
        max_eval = float('-inf')
        for child in get_children(board, 1):
            eval = minimax(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Prune the remaining branches
        return max_eval
    else:
        # Player 2's turn (minimize Player 1's score)
        min_eval = float('inf')
        for child in get_children(board, 2):
            eval = minimax(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Prune the remaining branches
        return min_eval





def evaluate_board(board, player):
    """Evaluate the board from the perspective of a specific player

    Args:
        board: The current game board
        player: The player for whom the evaluation is performed (either 1 or 2)

    Returns:
        A score representing the favorability of the board for the specified player
    """
    opponent = 2 if player == 1 else 1
    
    # Terminal states
    if check_win(board, player):
        return float('inf')  # player wins
    elif check_win(board, opponent):
        return float('-inf') # opponent wins
    elif is_draw(board):
        return 0             # draw
    
    # Otherwise use heuristic evaluation
    return heuristic(board, player)



def score_window(window, player):
    """Evaluate a window of 4 cells and assign a score based on token alignment

    Args: 
        window: A list of 4 consecutive cells from the board
        player: The player number (either 1 or 2)

    Returns:
        A score representing how favorable the window is for the player
    """
    opponent = 2 if player == 1 else 1
    score = 0

    # scoring for the players own opportunities (offensive play)
    if window.count(player) == 4:
        score += 1000
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 100
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10

    # scoring for threats by opponent (defensive play)
    if window.count(opponent) == 4:
        score -= 1500
    elif window.count(opponent) == 3 and window.count(0) == 1:
        score -= 100 # must block situation
    elif window.count(opponent) == 2 and window.count(0) == 2:
        score -= 10

    return score



def heuristic(board, player):
    """Evaluate the current board by adding up the scores from all possible 4-cell segments

    Args:
        board: The current game board
        player: The player number (1 or 2) whose perspective is used for evaluation

    Returns:
        A total heuristic score based on horizontal, vertical, and diagonal alignments
    """
    score = 0

    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = list(board[r, c:c+4])
            score += score_window(window, player)

    # vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            window = list(board[r:r+4, c])
            score += score_window(window, player)

    # positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i, c+i] for i in range(4)]
            score += score_window(window, player)

    # negative diagonal
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i, c+i] for i in range(4)]
            score += score_window(window, player)

    return score



def play_game_vs_ai(depth):
    """Connect 4: AI goes first (Player 1, Maximizer) and Human is Player 2 (Minimizer)

    Args:
        depth: The search depth for the AI's minimax algorithm
    """
    board = create_board()
    game_over = False

    print("Welcome to Connect 4 (AI goes first)!")
    print_board(board)

    while not game_over:

        # AI MOVE (PLAYER 1, MAXIMIZER)
        print("\nAI is thinking...")

        best_score = -math.inf   # AI maximizing
        best_col = None

        for c in range(COLS):
            if is_valid_location(board, c):
                r = get_next_open_row(board, c)
                temp_board = board.copy()
                drop_piece(temp_board, r, c, 1)

                score = minimax(temp_board, depth - 1, -math.inf, math.inf, False)

                if score > best_score:
                    best_score = score
                    best_col = c

        ai_row = get_next_open_row(board, best_col)
        drop_piece(board, ai_row, best_col, 1)

        print(f"\nAI chooses column {best_col}")
        print_board(board)

        # Check AI win or draw
        if check_win(board, 1):
            print("\nAI wins!")
            break
        if is_draw(board):
            print("\nIt's a draw!")
            break


        # HUMAN MOVE (PLAYER 2, MINIMIZER)
        valid_move = False
        while not valid_move:
            try:
                col = int(input(f"\nYour turn (0-{COLS-1}). Choose a column: "))
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            if is_valid_location(board, col):
                valid_move = True
            else:
                print("Column is full or out of bounds. Try again.")

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 2)
        print_board(board)

        # Check human win or draw
        if check_win(board, 2):
            print("\nYou win!")
            break
        if is_draw(board):
            print("\nIt's a draw!")
            break

    print("Game over.")



def main():
    print("========== CONNECT 4 AI ==========")
    print("AI (Player 1) vs You (Player 2)")
    print("----------------------------------")

    # Choose difficulty
    print("\nSelect AI Difficulty:")
    print("1 = Easy   (depth 2)")
    print("2 = Medium (depth 4)")
    print("3 = Hard   (depth 6)")

    while True:
        try:
            choice = int(input("Difficulty: "))
            if choice == 1:
                depth = 2
                break
            elif choice == 2:
                depth = 4
                break
            elif choice == 3:
                depth = 6
                break
            else:
                print("Enter a number from 1–3.")
        except ValueError:
            print("Invalid input. Enter a number.")

    print(f"\nStarting game with depth = {depth}...\n")
    play_game_vs_ai(depth)


if __name__ == "__main__":
    main()