from typing import Callable
import math

Turn = int
Board = list[list[int]]
Game = tuple[Board, Turn]

def min_value(state: Game, 
            evaluate_fn: Callable[[Game], float], 
            branch_fn: Callable[[Game], list[Game]]
           ) -> tuple[Game, float]:
    next_states = branch_fn(state)

    if len(next_states) == 0:
        return state, evaluate_fn(state)

    _, value = max_value(next_states[0], evaluate_fn, branch_fn)
    n_state = next_states[0]

    for i in range(1, len(next_states)):
        _, v = max_value(next_states[i], evaluate_fn, branch_fn)
        if v < value:
            value = v
            n_state = next_states[i]

    return n_state, value

def max_value(state: Game, 
            evaluate_fn: Callable[[Game], float], 
            branch_fn: Callable[[Game], list[Game]]
           ) -> tuple[Game, float]:
    next_states = branch_fn(state)

    if len(next_states) == 0:
        return state, evaluate_fn(state)

    _, value = min_value(next_states[0], evaluate_fn, branch_fn)
    n_state = next_states[0]

    for i in range(1, len(next_states)):
        s, v = min_value(next_states[i], evaluate_fn, branch_fn)
        if v > value:
            value = v
            n_state = next_states[i]

    return n_state, value

def jogo_velha_min_max(game: Game) -> Board:
    best_move, _ = max_value(game, evaluate_jogo_velha, branch_jogo_velha)
    return best_move[0]


def copy_board(board: Board) -> Board:
    new_b = []
    for line in board:
        l = []
        for square in line:
            l.append(square)
        new_b.append(l)

    return new_b

def branch_jogo_velha(game: Game) ->list[Game]:
    board, turn = game
    new_games: list[Game] = [] 

    # Test if game is over
    if (evaluate_jogo_velha(game) != 0):
        return new_games

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                new_b = copy_board(board)
                new_b[i][j] = turn
                new_games.append((new_b, turn * -1))

    return new_games

def evaluate_jogo_velha(game: Game) -> float:
    board, turn = game

    for i in range(len(board[0])):
        line_sum = 0
        for j in range(len(board)):
            line_sum += board[j][i]

        if line_sum == -3:
            return -1

        if line_sum == 3:
            return 1

    for line in board:
       if sum(line) == -3:
            return -1

       if sum(line) == 3:
            return 1
    
    diag_sum = board[0][0] + board[1][1] + board[2][2]
    if diag_sum == -3:
        return -1
    if diag_sum == 3:
        return 1

    diag_sum = board[0][2] + board[1][1] + board[2][0]
    if diag_sum == -3:
        return -1
    if diag_sum == 3:
        return 1

    return 0

def print_board(board: Board) -> None:
    for line in board:
        print(line)

def main() -> None:
    board = [
                [ 1,  1, -1],
                [-1, -1,  0],
                [ 1,  0,  0],
             ]
        
    print_board(jogo_velha_min_max((board, 1)))

if __name__ == "__main__":
    main()
