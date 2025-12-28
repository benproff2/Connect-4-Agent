import pygame as py
import sys
import math
from game_logic import *

# define the colors and dimensions
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 240, 240)
LIGHT_BLUE = (173, 216, 230)
WHEAT = (245, 222, 179)
RED = (255, 0, 0) # Player 1 (maximizing player)
YELLOW = (255, 255, 0) # Player 2 (minimizing player)
TEXT_COLOR = (0, 0, 0)

SQUARESIZE = 100 # size of each square cell
RADIUS = SQUARESIZE // 2 - 5 # radius of the pieces
STATUS_BAR_HEIGHT = 60 # for status message
HOVER_AREA_HEIGHT = 100 # for floating piece
BOTTOM_PADDING = 0 # prevent cut-off at bottom
SIDE_PADDING = 60 # balance left/right spacing
width = (COLS * SQUARESIZE) + SIDE_PADDING * 2 
height = STATUS_BAR_HEIGHT + HOVER_AREA_HEIGHT + (ROWS * SQUARESIZE) + BOTTOM_PADDING 
SIZE = (width, height) 


def draw_board(screen, board, FONT):
    """Draws the Connect 4 game board on the screen

    Args:
        screen: The Pygame display surface to draw on
        board: A 2D NumPy array representing the current state of the game board
        FONT: The Pygame font object for any text rendering
    """
    screen.fill(WHEAT)  

    board_offset_y = HOVER_AREA_HEIGHT  

    # draw the board grid and empty slots
    for c in range(COLS):
        for r in range(ROWS):
            x = SIDE_PADDING + c * SQUARESIZE
            y = board_offset_y + r * SQUARESIZE
            py.draw.rect(screen, BLUE, (x, y, SQUARESIZE, SQUARESIZE), border_radius=10)
            py.draw.circle(screen, WHEAT, (x + SQUARESIZE // 2, y + SQUARESIZE // 2), RADIUS)

    # draw the pieces on the board
    for c in range(COLS):
        for r in range(ROWS):
            val = board[r][c]
            if val == 0:
                continue

            if val == 1:
                color = RED
            else:
                color = YELLOW

            x = SIDE_PADDING + c * SQUARESIZE
            y = board_offset_y + r * SQUARESIZE
            py.draw.circle(screen, color, (x + SQUARESIZE // 2, y + SQUARESIZE // 2), RADIUS)

    py.display.update() # update the full display



def center_blit(screen, surface, y):
    """Center blit a surface on the screen at a given y-coordinate
    
    Args:
        screen: The Pygame display surface to draw on
        surface: The Pygame surface to be blitted
        y: The y-coordinate where the surface should be blitted
    """
    x = (width - surface.get_width()) // 2
    screen.blit(surface, (x, y))



def display_message(screen, FONT, text):
    """Display a message in the status bar area for 1.5 seconds

    Args:
        screen: The Pygame display surface to draw on
        FONT: The Pygame font object for text rendering
        text: The message text to display    
    """
    label = FONT.render(text, True, TEXT_COLOR)
    center_blit(screen, label, height - STATUS_BAR_HEIGHT + 10)
    py.display.update()
    py.time.wait(1500)




def animate_drop(screen, board, col, row, player, FONT):
    """Animate the dropping of a piece into the board

    Args:
        screen: The Pygame display surface to draw on
        board: The current game board
        col: The column index where the piece is dropped
        row: The row index where the piece lands
        player: The player number (1 or 2) whose piece is being dropped
        FONT: The Pygame font object for text rendering
    """
    color = RED if player == 1 else YELLOW
    x_center = SIDE_PADDING + col * SQUARESIZE + SQUARESIZE // 2
    board_offset_y = HOVER_AREA_HEIGHT
    target_y = board_offset_y + row * SQUARESIZE + SQUARESIZE // 2
    y = HOVER_AREA_HEIGHT // 2


    clock = py.time.Clock()
    while y < target_y:
        y += 20

        if y > target_y:
            y = target_y

        draw_board(screen, board, FONT)
        py.draw.circle(screen, color, (x_center, y), RADIUS)
        py.display.update()
        clock.tick(60)



def name_input_screen(screen, FONT):
    """Display the name input screen and return the entered player name

    Args:
        screen: The Pygame display surface to draw on
        FONT: The Pygame font object for text rendering
    """
    box_width = 400
    box_height = 80
    box_x = (width - box_width) // 2
    input_box = py.Rect(box_x, 250, box_width, box_height)
    player_name = ""
    active = False

    while True:
        screen.fill(LIGHT_BLUE)

        title = FONT.render("Welcome to Connect 4!", True, TEXT_COLOR)
        center_blit(screen, title, 100)

        prompt = FONT.render("Enter your name:", True, TEXT_COLOR)
        center_blit(screen, prompt, 180)

        py.draw.rect(screen, ORANGE, input_box, border_radius=10)
        text_surf = FONT.render(player_name, True, TEXT_COLOR)
        center_blit(screen, text_surf, input_box.y + 20)

        py.display.update()

        
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)

            if event.type == py.KEYDOWN and active:
                if event.key == py.K_RETURN:
                    if player_name != "":
                        return player_name
                    else: 
                        return "Player"
                elif event.key == py.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12:
                        player_name += event.unicode




def turn_select_screen(screen, FONT, name):
    """Display the turn selection screen and return the chosen turn order

    Args:
        screen: The Pygame display surface to draw on
        FONT: The Pygame font object for text rendering
        name: The player's name to personalize the prompt

    Returns:
        0 if the player chooses to go first, 1 if second
    """
    button_width = 400
    button_height = 80
    x_centered = (width - button_width) // 2

    first_rect = py.Rect(x_centered, 250, button_width, button_height)
    second_rect = py.Rect(x_centered, 350, button_width, button_height)

    while True:
        screen.fill(LIGHT_BLUE)

        title = FONT.render(f"{name}, choose turn order:", True, TEXT_COLOR)
        center_blit(screen, title, 100)

        first_label = FONT.render("Go FIRST", True, TEXT_COLOR)
        second_label = FONT.render("Go SECOND", True, TEXT_COLOR)

        py.draw.rect(screen, ORANGE, first_rect, border_radius=10)
        py.draw.rect(screen, ORANGE, second_rect, border_radius=10)

        center_blit(screen, first_label, first_rect.y + 20)
        center_blit(screen, second_label, second_rect.y + 20)

        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if first_rect.collidepoint(event.pos):
                    return 0 # player goes first
                if second_rect.collidepoint(event.pos):
                    return 1 # player goes second



def difficulty_screen(screen, FONT):
    """Display the difficulty selection screen and return the chosen depth

    Args:
        screen: The Pygame display surface to draw on
        FONT: The Pygame font object for text rendering

    Returns:
        The search depth corresponding to the selected difficulty
    """
    button_width = 500
    button_height = 80
    x_centered = (width - button_width) // 2

    easy_rect = py.Rect(x_centered, 200, button_width, button_height)
    med_rect = py.Rect(x_centered, 300, button_width, button_height)
    hard_rect = py.Rect(x_centered, 400, button_width, button_height)

    while True:
        screen.fill(LIGHT_BLUE)

        title = FONT.render("Select Difficulty", True, TEXT_COLOR)
        center_blit(screen, title, 80)

        # labels for each button
        easy_lbl = FONT.render("Easy (Depth 2)", True, TEXT_COLOR)
        med_lbl = FONT.render("Medium (Depth 4)", True, TEXT_COLOR)
        hard_lbl = FONT.render("Hard (Depth 6)", True, TEXT_COLOR)

        # buttons for each difficulty
        py.draw.rect(screen, ORANGE, easy_rect, border_radius=10)
        py.draw.rect(screen, ORANGE, med_rect, border_radius=10)
        py.draw.rect(screen, ORANGE, hard_rect, border_radius=10)

        center_blit(screen, easy_lbl, easy_rect.y + (button_height - easy_lbl.get_height()) // 2)
        center_blit(screen, med_lbl, med_rect.y + (button_height - med_lbl.get_height()) // 2)
        center_blit(screen, hard_lbl, hard_rect.y + (button_height - hard_lbl.get_height()) // 2)

        py.display.update() # update the full display

        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos): 
                    return 2 
                if med_rect.collidepoint(event.pos): 
                    return 4
                if hard_rect.collidepoint(event.pos): 
                    return 6



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



def minimax_with_col(board, depth, alpha, beta, maximizing, ai_player):
    """Recursively evaluates game states using the Minimax algorithm with Alpha-Beta pruning.
        This version returns both the best column choice and the evaluated score.

    Args:
        board: The current game board
        depth: How many layers deep to search
        alpha: The alpha value used for pruning
        beta: The beta value used for pruning
        maximizing: True if evaluating the maximizing player (AI), False if minimizing
        ai_player: The player number representing the AI (1 or 2)

    Returns:
        A tuple (best_col, score) where:
            best_col is the column index of the strongest move,
            score is the evaluated score of that move.
    """
    valid_locations = [c for c in range(COLS) if is_valid_location(board, c)] # list of valid columns
    terminal = check_win(board, 1) or check_win(board, 2) or is_draw(board) # terminal state check

    if depth == 0 or terminal:
        return None, heuristic(board, ai_player)

    # maximizing player
    if maximizing:
        value = -math.inf
        best_col = valid_locations[0] # default to first valid column
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp = board.copy()
            drop_piece(temp, row, col, ai_player)
            _, score = minimax_with_col(temp, depth-1, alpha, beta, False, ai_player) # recursive call for minimizing player
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        # minimizing player
        value = math.inf
        opponent = 1 if ai_player == 2 else 2
        best_col = valid_locations[0] # default to first valid column
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp = board.copy()
            drop_piece(temp, row, col, opponent)
            _, score = minimax_with_col(temp, depth-1, alpha, beta, True, ai_player) # recursive call for maximizing player
            if score < value:
                value = score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value



def end_screen(screen, FONT):
    """Display the end game screen with options to play again or quit

    Args:
        screen: The Pygame display surface to draw on
        FONT: The Pygame font object used for rendering text
    """
    py.time.wait(1500)

    button_width = 400
    button_height = 80
    x_centered = (width - button_width) // 2

    play_again_rect = py.Rect(x_centered, 300, button_width, button_height)
    quit_rect = py.Rect(x_centered, 400, button_width, button_height)

    while True:
        screen.fill(LIGHT_BLUE)

        title = FONT.render("Game Over!", True, TEXT_COLOR)
        center_blit(screen, title, 100)

        play_again_lbl = FONT.render("Play Again", True, TEXT_COLOR)
        quit_lbl = FONT.render("Quit", True, TEXT_COLOR)

        py.draw.rect(screen, ORANGE, play_again_rect)
        py.draw.rect(screen, ORANGE, quit_rect)

        center_blit(screen, play_again_lbl, play_again_rect.y + 20)
        center_blit(screen, quit_lbl, quit_rect.y + 20)

        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    run_pygame_game()
                if quit_rect.collidepoint(event.pos):
                    sys.exit()



def update_status_text(screen, text, FONT):
    """Update the status bar text at the bottom of the screen

    Args:
        screen: The Pygame display surface to draw on
        text: The status message text to display
        FONT: The Pygame font object for rendering text
    """
    py.draw.rect(screen, WHEAT, (0, height - STATUS_BAR_HEIGHT, width, STATUS_BAR_HEIGHT))
    label = FONT.render(text, True, TEXT_COLOR)
    center_blit(screen, label, height - STATUS_BAR_HEIGHT + 10)
    py.display.update()



def run_pygame_game():
    """Run the main Connect 4 game loop using Pygame
    """
    py.init()
    FONT = py.font.SysFont("monospace", 50)

    screen = py.display.set_mode(SIZE)
    py.display.set_caption("Connect 4")

    # Initial setup screens
    name = name_input_screen(screen, FONT)
    turn = turn_select_screen(screen, FONT, name)
    depth = difficulty_screen(screen, FONT)

    board = create_board()
    draw_board(screen, board, FONT)
    game_over = False

    # determine player roles
    human = 1 if turn == 0 else 2
    ai = 2 if human == 1 else 1
    current_turn = 0 if turn == 0 else 1  # 0 = human, 1 = AI

    update_status_text(screen, f"{name}, it's your turn." if current_turn == 0 else "AI is thinking...", FONT)

    # main game loop
    while not game_over:

        # HUMAN TURN
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

            if event.type == py.MOUSEMOTION and current_turn == 0:
                py.draw.rect(screen, WHEAT, (0, 0, width, HOVER_AREA_HEIGHT))

                # calculate column under the mouse
                posx = event.pos[0]
                col = (posx - SIDE_PADDING) // SQUARESIZE

                col = max(0, min(COLS - 1, col)) # clamp the columns to make sure it doesn't go out of bounds on the screen
                x_center = SIDE_PADDING + col * SQUARESIZE + SQUARESIZE // 2 # center of the column

                hover_color = RED if human == 1 else YELLOW
                py.draw.circle(screen, hover_color, (x_center, HOVER_AREA_HEIGHT // 2), RADIUS)
                py.display.update()

            if event.type == py.MOUSEBUTTONDOWN and current_turn == 0:
                posx = event.pos[0]
                col = (posx - SIDE_PADDING) // SQUARESIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    animate_drop(screen, board, col, row, human, FONT)
                    drop_piece(board, row, col, human)
                    draw_board(screen, board, FONT)
                    update_status_text(screen, f"{name} chose column {col}", FONT)

                    if check_win(board, human):
                        draw_board(screen, board, FONT)
                        display_message(screen, FONT, f"{name} Wins!")
                        game_over = True
                        break

                    if is_draw(board):
                        draw_board(screen, board, FONT)
                        display_message(screen, FONT, "It's a Draw!")
                        game_over = True
                        break

                    current_turn = 1
                    update_status_text(screen, "AI is thinking...", FONT)


        # AI TURN
        if current_turn == 1 and not game_over:
            py.time.wait(600)

            best_col, _ = minimax_with_col(board, depth, -math.inf, math.inf, True, ai)

            if best_col is not None and is_valid_location(board, best_col):
                ai_row = get_next_open_row(board, best_col)
                animate_drop(screen, board, best_col, ai_row, ai, FONT)
                drop_piece(board, ai_row, best_col, ai)
                draw_board(screen, board, FONT)
                update_status_text(screen, f"AI chose column {best_col}", FONT)

                if check_win(board, ai):
                    draw_board(screen, board, FONT)
                    display_message(screen, FONT, "AI Wins!")
                    game_over = True
                    break

                if is_draw(board):
                    draw_board(screen, board, FONT)
                    display_message(screen, FONT, "It's a Draw!")
                    game_over = True
                    break

                current_turn = 0
                update_status_text(screen, f"{name}, it's your turn.", FONT)

    # end game screen
    py.time.wait(1500)
    end_screen(screen, FONT)



def main():
    run_pygame_game()


if __name__ == "__main__":
    main()