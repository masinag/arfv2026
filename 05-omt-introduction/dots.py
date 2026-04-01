from pysmt.shortcuts import (
    GE,
    LE,
    And,
    Equals,
    Int,
    Ite,
    Plus,
    Solver,
    Symbol,
)
from pysmt.typing import INT


def print_model(model):
    colors = {
        E: "",
        R: "\x1b[31m",
        Y: "\x1b[33m",
        B: "\x1b[34m",
        G: "\x1b[32m",
    }
    end = "\033[0m "
    C = "⏺"
    S = "🞄"
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(
                f"{colors[model[xx[i][j]]]}{S if grid[i][j]==E else C}",
                end=end,
            )
        print()


def neighbors(i, j):
    return [
        xx[ni][nj]
        for inci, incj in [(-1, 0), (0, 1), (1, 0), (0, -1)]
        if 0 <= (ni := i + inci) < len(grid)
        and 0 <= (nj := j + incj) < len(grid[0])
    ]


E = Int(0)
R = Int(1)
Y = Int(2)
B = Int(3)
G = Int(4)

grid = [
    [R, Y, E, E, E],
    [E, E, E, B, E],
    [E, B, Y, E, E],
    [E, G, E, E, E],
    [E, E, E, R, G],
]

xx = [
    [Symbol(f"x{i}{j}", INT) for j in range(len(grid[0]))]
    for i in range(len(grid))
]


assertions = []

# restrict cells values
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == E:
            assertions.append(
                And(GE(xx[i][j], E), LE(xx[i][j], G))
            )
        else:
            assertions.append(Equals(xx[i][j], grid[i][j]))

# every empty cell must have one incoming and one outgoing cells of the same color
# every non-empty cell must have one incoming/outgoing cell of the same color
for i in range(len(grid)):
    for j in range(len(grid[0])):
        nn = neighbors(i, j)
        num_equals_neighs = 2 if grid[i][j] == E else 1

        assertions.append(
            Equals(
                Int(num_equals_neighs),
                Plus(
                    Ite(Equals(xx[i][j], n), Int(1), Int(0))
                    for n in nn
                ),
            )
        )


with Solver("msat") as solver:
    solver.add_assertions(assertions)
    if solver.solve():
        print_model(solver.get_model())
    else:
        print("UNSAT")
