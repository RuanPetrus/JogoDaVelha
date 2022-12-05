# Jogo da Velha Min Max
Primeiramente foi implementado funções genéricas de min e max.
```python
def min_value(
    state: Game,
    evaluate_fn: Callable[[Game], float],
    branch_fn: Callable[[Game], List[Game]],
) -> float:

    next_states = branch_fn(state)

    if len(next_states) == 0:
        return evaluate_fn(state)

    max_value_fn = partial(max_value, evaluate_fn=evaluate_fn, branch_fn=branch_fn)
    return min(map(max_value_fn, next_states))


def max_value(
    state: Game,
    evaluate_fn: Callable[[Game], float],
    branch_fn: Callable[[Game], List[Game]],
) -> float:

    next_states = branch_fn(state)

    if len(next_states) == 0:
        return evaluate_fn(state)

    min_value_fn = partial(min_value, evaluate_fn=evaluate_fn, branch_fn=branch_fn)
    return max(map(min_value_fn, next_states))
```

Onde elas recebem uma função que gera os próximos movimentos, chamada _branch\_fn_ e uma função que faz a evaluação do estado caso seja um nó folha, chamada _evaluate\_fn_, .A função _max\_value_ retorna o máximo valor possível dos movimentos que a _min\_value_retorna e vice e versa.

Depois foi feita a implementação dessas funções e do estado que representam o jogo da velha.
```python
Player = Literal[-1, 0, 1]
Turn = Literal[1, -1]
Board = List[List[int]]
Game = Tuple[Board, Turn]

lookup = {
    1: "X",
    -1: "O",
    0: " ",
}

def get_winner(board: Board) -> Optional[Player]:
    def is_board_complete() -> bool:
        zero_squares = [s for line in board for s in line if s == 0]
        return len(zero_squares) == 0

    vertical = [[board[i][j] for i in range(len(board[0]))] for j in range(len(board))]
    horizontal = board
    diagonal = [
        [board[i][i] for i in range(len(board))],
        [board[i][abs(i - 2)] for i in range(len(board))],
    ]

    result = [
        line
        for line in vertical + horizontal + diagonal
        if sum(line) == 3 or sum(line) == -3
    ]

    if len(result) == 0:
        if is_board_complete():
            return 0
        return None

    if result[0][0] == -1:
        return -1

    return 1


def evaluate_jogo_velha(game: Game) -> float:
    board, _ = game
    result = get_winner(board)

    if result is None:
        raise ValueError("Game is not finished")

    return result


def branch_jogo_velha(game: Game) -> List[Game]:
    board, turn = game
    new_games: List[Game] = []

    # If game is over return [] leaf node
    if get_winner(board) is not None:
        return new_games

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                new_b = copy_board(board)
                new_b[i][j] = turn
                new_games.append((new_b, -turn))

    return new_games

```
A função auxiliar _get\_winner_, retorna _None_ caso o jogo ainda não tenha acabado _1_ caso o _X_ vença, _-1_ caso o _O_ vença e _0_ caso tenha dado velha.

A função _branch\_jogo_velha_ utiliza a função auxiliar para saber se o jogo acabou caso não ela gera os próximos possíveis jogos.

A função _evaluate\_jogo\_velha_ utiliza a função _get\_winner_ e retorna o mesmo valor.

Depois disso basta apenas juntar tudo isso em uma função que liga os valores recebidos das funções min max com o próximo melhor movimento que é feito na função _min\_max\_jogo\_velha_.

```python
def jogo_velha_min_max(game: Game) -> Board:
    _, turn = game

    assert turn == 1 or turn == -1, "Turn must be 1 or -1"

    if turn == 1:
        min_value_fn = partial(
            min_value, evaluate_fn=evaluate_jogo_velha, branch_fn=branch_jogo_velha
        )

        possible_games = max(
            map(lambda g: (min_value_fn(g), g), branch_jogo_velha(game))
        )
    else:
        max_value_fn = partial(
            max_value, evaluate_fn=evaluate_jogo_velha, branch_fn=branch_jogo_velha
        )
        possible_games = min(
            map(lambda g: (max_value_fn(g), g), branch_jogo_velha(game))
        )

    return possible_games[1][0]
```
Podemos ver um programa completo que uma IA joga contra si mesma abaixo.

```python
from functools import partial
from typing import Callable, List, Tuple, Optional, Literal

Player = Literal[-1, 0, 1]
Turn = Literal[1, -1]
Board = List[List[int]]
Game = Tuple[Board, Turn]

lookup = {
    1: "X",
    -1: "O",
    0: " ",
}


def min_value(
    state: Game,
    evaluate_fn: Callable[[Game], float],
    branch_fn: Callable[[Game], List[Game]],
) -> float:

    next_states = branch_fn(state)

    if len(next_states) == 0:
        return evaluate_fn(state)

    max_value_fn = partial(max_value, evaluate_fn=evaluate_fn, branch_fn=branch_fn)
    return min(map(max_value_fn, next_states))


def max_value(
    state: Game,
    evaluate_fn: Callable[[Game], float],
    branch_fn: Callable[[Game], List[Game]],
) -> float:

    next_states = branch_fn(state)

    if len(next_states) == 0:
        return evaluate_fn(state)

    min_value_fn = partial(min_value, evaluate_fn=evaluate_fn, branch_fn=branch_fn)
    return max(map(min_value_fn, next_states))


def jogo_velha_min_max(game: Game) -> Board:
    _, turn = game

    assert turn == 1 or turn == -1, "Turn must be 1 or -1"

    if turn == 1:
        min_value_fn = partial(
            min_value, evaluate_fn=evaluate_jogo_velha, branch_fn=branch_jogo_velha
        )

        possible_games = max(
            map(lambda g: (min_value_fn(g), g), branch_jogo_velha(game))
        )
    else:
        max_value_fn = partial(
            max_value, evaluate_fn=evaluate_jogo_velha, branch_fn=branch_jogo_velha
        )
        possible_games = min(
            map(lambda g: (max_value_fn(g), g), branch_jogo_velha(game))
        )

    return possible_games[1][0]


def copy_board(board: Board) -> Board:
    new_b = []
    for line in board:
        l = []
        for square in line:
            l.append(square)
        new_b.append(l)

    return new_b


def branch_jogo_velha(game: Game) -> List[Game]:
    board, turn = game
    new_games: List[Game] = []

    # If game is over return [] leaf node
    if get_winner(board) is not None:
        return new_games

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                new_b = copy_board(board)
                new_b[i][j] = turn
                new_games.append((new_b, -turn))

    return new_games


def get_winner(board: Board) -> Optional[Player]:
    def is_board_complete() -> bool:
        zero_squares = [s for line in board for s in line if s == 0]
        return len(zero_squares) == 0

    vertical = [[board[i][j] for i in range(len(board[0]))] for j in range(len(board))]
    horizontal = board
    diagonal = [
        [board[i][i] for i in range(len(board))],
        [board[i][abs(i - 2)] for i in range(len(board))],
    ]

    result = [
        line
        for line in vertical + horizontal + diagonal
        if sum(line) == 3 or sum(line) == -3
    ]

    if len(result) == 0:
        if is_board_complete():
            return 0
        return None

    if result[0][0] == -1:
        return -1

    return 1


def evaluate_jogo_velha(game: Game) -> float:
    board, _ = game
    result = get_winner(board)

    if result is None:
        raise ValueError("Game is not finished")

    return result


def print_board(board: Board) -> None:
    for line in board:
        print([lookup[s] for s in line])


def main() -> None:
    board: Board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    turn = 1
    while get_winner(board) is None:
        board = jogo_velha_min_max((board, turn))
        turn = -turn
        print_board(board)
        print("------------------")


if __name__ == "__main__":
    main()

```


