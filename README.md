# B351 Fall 2025 Final Project - Connect 4 AI Agent

## Group Members:
- Alan Gawrys
- Bennett Proffitt


## Course Instructors:
- Yijie Wang - yijwang (Mentor)
- Yang - yw109
- Leo - zwu1
- Hasan - mshlib


## Description:
This project implements an AI agent that plays the game of Connect 4 using the **Minimax algorithm** with **Alpha-Beta pruning**. The agent can be played in both a terminal environment and a graphical interface using **Pygame**.  

We also created visualizations (in `.png` format) to evaluate the agent’s performance, such as runtime vs. depth and board state heatmaps. These were generated using the `connect4_evaluation.py` file.

## File Overview

### `game_logic.py`
Handles the core mechanics of Connect 4, such as board creation, piece placement, move validation, win detection, and generating possible board states.  
If not already installed, it is recommended to install `numpy` on your device.

**Functions:**
- `create_board()` – Initializes an empty 6x7 game board using NumPy.
- `print_board(board)` – Displays the current board state in a readable format.
- `is_valid_location(board, col)` – Checks if a move in a given column is valid.
- `get_next_open_row(board, col)` – Finds the next empty row in the specified column.
- `drop_piece(board, row, col, player)` – Places a player’s piece at the given position.
- `check_win(board, player)` – Checks if the specified player has won (4 in a row).
- `is_draw(board)` – Determines if the board is full with no winner (a draw).
- `get_children(board, player)` – Generates all possible next board states for the current player.

---

### `ai_terminal.py`
Implements the AI logic and provides a terminal-based interface to play Connect 4 against the computer.  
This file uses the **Minimax algorithm** with **Alpha-Beta pruning** to make strategic decisions.

To play the game in the terminal, simply run the file itself: `python ai_terminal.py`.  
It is recommended to use **Python 3.12.3** for full compatibility.

**Functions:**
- `minimax(board, depth, alpha, beta, maximizing_player)` – Recursively evaluates board states using Minimax with Alpha-Beta pruning.
- `evaluate_board(board, player)` – Scores terminal game states (win, lose, draw) from a specific player’s perspective.
- `score_window(window, player)` – Assigns a score to a 4-cell window based on offensive and defensive heuristics.
- `heuristic(board, player)` – Calculates a total score for the board by analyzing horizontal, vertical, and diagonal sequences.
- `play_game_vs_ai(depth)` – Runs the actual gameplay between the human and AI in the terminal.
- `main()` - Handles difficulty selection (easy, medium, hard) and launches the game.

**Example:**
Here's a showcase of the terminal interface when running `ai_terminal.py`:

<div align="center">

<table>
  <tr>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/80a5e37b-9c1d-4faf-9b3f-b0e44babfb1f" width="400"/>
      <br><sub><b>(a)</b> The game begins with an empty board and prompts the user to choose difficulty.</sub>
    </td>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/0711b73a-af9c-4615-806a-7b2475c2fe39" width="400"/>
      <br><sub><b>(b)</b> An example of an AI win with the final board state.</sub>
    </td>
  </tr>
</table>

</div>

---

### `pygame_gui.py`

Creates a graphical interface (GUI) for playing Connect 4 using **Pygame**, allowing the user to interact with the board visually by clicking on columns.
This file also uses the **Minimax algorithm** with **Alpha-Beta pruning** to make strategic decisions for the AI opponent.  

If not already installed, it is recommended to install `pygame`, `sys`, and `numpy` (from `game_logic.py`) on your device.  
It is **required** to use **Python 3.12.3** for full compatibility.  

To play the game, simply run the file itself: `python pygame_gui.py`.  




**Functions:**

- `draw_board(screen, board, FONT)` — Renders the game board and pieces.
- `center_blit(screen, surface, y)` — Blits a surface centered horizontally at a specified vertical position.
- `display_message(screen, FONT, text)` — Shows a temporary message in the status bar.
- `animate_drop(screen, board, col, row, player, FONT)` — Animates a token dropping into a column.
- `name_input_screen(screen, FONT)` — Prompts the player to enter their name.
- `turn_select_screen(screen, FONT, name)` — Lets the player choose who goes first.
- `difficulty_screen(screen, FONT)` — Provides difficulty selection and maps it to search depth.
- `score_window(window, player)` — Assigns a score to a 4-cell window for heuristics.
- `heuristic(board, player)` — Evaluates the entire board’s score for a player.
- `minimax_with_col(board, depth, alpha, beta, maximizing, ai_player)` — Minimax with alpha-beta pruning, returns best column and score.
- `end_screen(screen, FONT)` — Displays end screen options to replay or quit.
- `update_status_text(screen, text, FONT)` — Updates the status message at the bottom of the screen.
- `run_pygame_game()` — Main game loop that handles logic and rendering.
- `main()` — Calls `run_pygame_game()`.




**Example:** Here's a showcase of the GUI interface when running `pygame_gui.py`:


<div align="center">

<table>
  <tr>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/eb91ccb8-f74d-4f7a-af5f-d519090304fb" width="300"/><br/>
      <em>(a) Name Entry</em>
    </td>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/faaed427-a99e-4101-85fe-72a7132f108f" width="300"/><br/>
      <em>(b) Select Turn Order</em>
    </td>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/2f621758-2057-4293-b9fd-0a6b6d4355f5" width="300"/><br/>
      <em>(c) Choose Difficulty</em>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/c9f5dbc2-c516-4ae5-897b-24482b58dd76" width="300"/><br/>
      <em>(d) Game start</em>
    </td>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/53a571e9-5bac-4030-b7e2-3fc31270ed6a" width="300"/><br/>
      <em>(e) Mid Game</em>
    </td>
    <td align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/901ed440-a25b-47be-9f4f-9d9c84a7071c" width="300"/><br/>
      <em>(f) Game Ende</em>
    </td>
  </tr>
  <tr>
    <td colspan="3" align="center">
      <img src="https://github.iu.edu/agawrys/B351-Fall2025-FinalProject-agawrys-benproff/assets/23694/b48a82a6-0a3b-439e-864f-1e23e6ab3806" width="300"/><br/>
      <em>(g) Quit Screen</em>
    </td>
  </tr>
</table>

</div>


---

### `connect4_evaluation.py`

Evaluates the performance of the **Minimax algorithm**, both **with and without Alpha-Beta pruning**, by measuring execution time and the number of nodes expanded across different search depths.  
This file is primarily used for generating performance visualizations related to AI evaluation in Connect 4.

If not already installed, it is recommended to install `matplotlib`.  
It is **required** to use **Python 3.11.5** for full compatibility.  

To run the evaluation file, simply run the file itself: `python connect4_evaluation.py`.  

Upon execution, the following visualizations were generated and put into the `visualizations/` folder in this repository:

 - **heatmap_board_eval.png** — A heatmap showing heuristic evaluation scores across various search depths for random board states.

 - **nodes_vs_depth.png** — A line chart comparing the number of nodes expanded with and without alpha-beta pruning (log scale).

 - **time_vs_depth.png** — A line chart showing the time taken by Minimax with alpha-beta pruning at increasing depths.

These visualizations help analyze the computational efficiency and behavior of the AI under different configurations.


