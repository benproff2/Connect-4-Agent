import time
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt

from game_logic import (
    create_board,
    get_children,
    is_draw,
    check_win,
    drop_piece,
    get_next_open_row,
    is_valid_location,
    ROWS,
    COLS,
)
from ai_terminal import heuristic



def minimax_no_pruning(board, depth, maximizing_player, counter):
    """Minimax algorithm without alpha-beta pruning
    
    Args:
        board: Current game board state
        depth: Current depth in the game tree
        maximizing_player: True if the current turn is for the maximizing player
        counter: Dictionary to count the number of nodes expanded

    Returns:
        The heuristic value of the board.
    """
    counter['nodes'] += 1
    if depth == 0 or check_win(board, 1) or check_win(board, 2) or is_draw(board):
        return heuristic(board, 1)
    
    if maximizing_player:
        value = float('-inf')
        for child in get_children(board, 1):
            v = minimax_no_pruning(child, depth - 1, False, counter)
            if v > value:
                value = v
        return value
    else:
        value = float('inf')
        for child in get_children(board, 2):
            v = minimax_no_pruning(child, depth - 1, True, counter)
            if v < value:
                value = v
        return value



def minimax_ab(board, depth, alpha, beta, maximizing_player, counter):
    """Minimax algorithm with alpha-beta pruning

    Args:
        board: Current game board state
        depth: Current depth in the game tree
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        maximizing_player: True if the current turn is for the maximizing player
        counter: Dictionary to count the number of nodes expanded

    Returns:
        The heuristic value of the board
    """
    counter['nodes'] += 1
    if depth == 0 or check_win(board, 1) or check_win(board, 2) or is_draw(board):
        return heuristic(board, 1)
    
    if maximizing_player:
        value = float('-inf')
        for child in get_children(board, 1):
            v = minimax_ab(child, depth - 1, alpha, beta, False, counter)
            if v > value:
                value = v
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return value
    else:
        value = float('inf')
        for child in get_children(board, 2):
            v = minimax_ab(child, depth - 1, alpha, beta, True, counter)
            if v < value:
                value = v
            beta = min(beta, v)
            if beta <= alpha:
                break
        return value



def generate_random_board(seed=None, moves=8):
    """Generate a random Connect4 board by simulating a number of random moves

    Args:
        seed: Random seed for reproducibility
        moves: Number of random moves to simulate

    Returns:
        A Connect4 board with the specified number of random moves played
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    board = create_board()
    player = random.choice([1, 2])
    moves_played = 0

    while moves_played < moves:
        valid_cols = [c for c in range(COLS) if is_valid_location(board, c)]

        if not valid_cols:
            break

        col = random.choice(valid_cols)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

        if check_win(board, player):
            board[row, col] = 0
            break

        player = 1 if player == 2 else 2
        moves_played += 1

    return board



def generate_test_boards(num_boards=6, moves_range=(6, 12), seed=42):
    """Generate a list of random test boards for evaluation

    Args:
        num_boards: Number of test boards to generate
        moves_range: Tuple indicating the min and max number of moves for each board
        seed: Random seed for reproducibility

    Returns:
        A list of Connect4 boards
    """
    boards = []
    random.seed(seed)

    for i in range(num_boards):
        moves = random.randint(moves_range[0], moves_range[1])
        boards.append(generate_random_board(seed=seed + i, moves=moves))

    return boards



def run_experiments(
    depths=tuple(range(1, 9)),
    num_boards_for_heatmap=6,
    heatmap_depths=tuple(range(1, 9)),
    runs_per_depth=1,
    seed=1234,
):
    """Run experiments to measure time and nodes expanded for minimax with alpha-beta pruning

    Args:
        depths: Tuple of search depths to evaluate
        num_boards_for_heatmap: Number of random boards to generate for heatmap evaluation
        heatmap_depths: Tuple of depths to evaluate for heatmap
        runs_per_depth: Number of runs per depth for averaging
        seed: Random seed for reproducibility

    Returns:
        A dictionary containing experiment results
    """
    heatmap_boards = generate_test_boards(num_boards=num_boards_for_heatmap, seed=seed)
    times = []
    nodes_no_prune = []
    nodes_with_prune = []

    for depth in depths:
        t_total = 0.0
        nodes_ab_total = 0
        nodes_np_total = 0

        for run in range(runs_per_depth):
            root = create_board()
            counter_ab = {'nodes': 0}
            t0 = time.perf_counter()
            _ = minimax_ab(root.copy(), depth, float('-inf'), float('inf'), True, counter_ab)
            t1 = time.perf_counter()
            t_total += (t1 - t0)
            nodes_ab_total += counter_ab['nodes']
            counter_np = {'nodes': 0}
            _ = minimax_no_pruning(root.copy(), depth, True, counter_np)
            nodes_np_total += counter_np['nodes']

        avg_t = t_total / runs_per_depth
        avg_ab_nodes = nodes_ab_total / runs_per_depth
        avg_np_nodes = nodes_np_total / runs_per_depth
        times.append(avg_t)
        nodes_with_prune.append(avg_ab_nodes)
        nodes_no_prune.append(avg_np_nodes)
        print(f"Depth {depth}: time={avg_t:.4f}s, nodes_ab={avg_ab_nodes}, nodes_no_prune={avg_np_nodes}")

    heatmap = np.zeros((len(heatmap_boards), len(heatmap_depths)), dtype=float)

    for i, b in enumerate(heatmap_boards):
        for j, d in enumerate(heatmap_depths):
            counter_dummy = {'nodes': 0}
            score = minimax_ab(b.copy(), d, float('-inf'), float('inf'), True, counter_dummy)
            heatmap[i, j] = score

    results = {
        'depths': list(depths),
        'times': times,
        'nodes_ab': nodes_with_prune,
        'nodes_no_prune': nodes_no_prune,
        'heatmap_boards': heatmap_boards,
        'heatmap_matrix': heatmap,
        'heatmap_depths': list(heatmap_depths),
    }
    
    return results



def plot_time_vs_depth(depths, times, outpath="time_vs_depth.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(depths, times, marker='o')
    plt.xlabel("Search depth (plies)")
    plt.ylabel("Time (seconds)")
    plt.title("Time vs Search Depth (Alpha-Beta)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(depths)
    plt.savefig(outpath, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"Saved {outpath}")



def plot_nodes_vs_depth(depths, nodes_no_prune, nodes_ab, outpath="nodes_vs_depth.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(depths, nodes_no_prune, marker='o', label='No pruning')
    plt.plot(depths, nodes_ab, marker='s', label='Alpha-Beta')
    plt.yscale('log')
    plt.xlabel("Search depth (plies)")
    plt.ylabel("Nodes expanded (log scale)")
    plt.title("Nodes Expanded vs Search Depth")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(depths)
    plt.savefig(outpath, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"Saved {outpath}")



def plot_heatmap(matrix, rows_labels, col_labels, outpath="heatmap_board_eval.png"):
    plt.figure(figsize=(len(col_labels) * 1.1 + 2, len(rows_labels) * 0.6 + 2))
    im = plt.imshow(matrix, aspect='auto', interpolation='nearest')
    plt.colorbar(im)
    plt.xticks(ticks=np.arange(len(col_labels)), labels=col_labels)
    plt.yticks(ticks=np.arange(len(rows_labels)), labels=[f"B{i}" for i in range(len(rows_labels))])
    plt.xlabel("Search depth (plies)")
    plt.ylabel("Test board")
    plt.title("Board evaluation scores across depths (Player 1 perspective)")
    plt.savefig(outpath, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"Saved {outpath}")



def main():
    parser = argparse.ArgumentParser(description="Connect4 visualization experiments")
    parser.add_argument(
        "--depths",
        type=int,
        nargs="+",
        default=list(range(1, 9)),
    )
    parser.add_argument(
        "--heatmap_depths",
        type=int,
        nargs="+",
        default=list(range(1, 9)),
    )
    parser.add_argument("--num_boards", type=int, default=6)
    parser.add_argument("--runs_per_depth", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1234)
    args = parser.parse_args()
    depths = tuple(args.depths)
    heatmap_depths = tuple(args.heatmap_depths)
    results = run_experiments(
        depths=depths,
        num_boards_for_heatmap=args.num_boards,
        heatmap_depths=heatmap_depths,
        runs_per_depth=args.runs_per_depth,
        seed=args.seed,
    )
    plot_time_vs_depth(results['depths'], results['times'], outpath="time_vs_depth.png")
    plot_nodes_vs_depth(results['depths'], results['nodes_no_prune'], results['nodes_ab'], outpath="nodes_vs_depth.png")
    plot_heatmap(results['heatmap_matrix'], results['heatmap_boards'], results['heatmap_depths'], outpath="heatmap_board_eval.png")
    print("All visualizations created.")


if __name__ == "__main__":
    main()