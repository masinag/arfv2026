from pysmt.fnode import FNode
from pysmt.shortcuts import And, ExactlyOne, Int, Solver, Symbol
from pysmt.typing import INT

N = 5
G = [[Symbol(f"x{i}{j}", INT) for j in range(N)] for i in range(N)]
EMPTY, BALL, IRON, BLACK = map(Int, range(4))

AREAS = [
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1)],
    [(1, 1), (2, 1), (3, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(1, 3), (2, 3), (3, 3)],
    [(0, 3), (0, 4), (1, 4), (2, 4)],
    [(4, 2), (4, 3), (4, 4)],
]
BLACK_COORDS = [(0, 1), (3, 2), (3, 4)]


def domain_constraints() -> list[FNode]:
    cc = []
    for i in range(N):
        for j in range(N):
            if (i, j) in BLACK_COORDS:
                cc.append(G[i][j].Equals(BLACK))
            else:
                cc.append(
                    G[i][j].Equals(EMPTY) | G[i][j].Equals(BALL) | G[i][j].Equals(IRON)
                )
    return cc


def one_per_area(item: FNode) -> list[FNode]:
    return [ExactlyOne(G[i][j].Equals(item) for i, j in area) for area in AREAS]


def balloons_are_light() -> list[FNode]:
    cc = []
    for i in range(1, N):
        for j in range(N):
            cc.append(
                G[i][j]
                .Equals(BALL)
                .Implies(G[i - 1][j].Equals(BALL) | G[i - 1][j].Equals(BLACK))
            )
    return cc


def iron_is_heavy() -> list[FNode]:
    cc = []
    for i in range(0, N - 1):
        for j in range(N):
            cc.append(
                G[i][j]
                .Equals(IRON)
                .Implies(G[i + 1][j].Equals(IRON) | G[i + 1][j].Equals(BLACK))
            )
    return cc


def print_sol(model):
    print("Solution:")
    for i in range(5):
        for j in range(5):
            if model[G[i][j]] == EMPTY:
                print(" ", end="")
            elif model[G[i][j]] == BALL:
                print("O", end="")
            elif model[G[i][j]] == IRON:
                print("I", end="")
            elif model[G[i][j]] == BLACK:
                print("B", end="")
        print()


def main():
    assertions = []
    assertions += domain_constraints()
    assertions += one_per_area(BALL)
    assertions += one_per_area(IRON)
    assertions += balloons_are_light()
    assertions += iron_is_heavy()
    with Solver() as solver:
        solver.add_assertions(assertions)
        if solver.solve():
            model = solver.get_model()
            print_sol(model)
            solver.add_assertion(
                ~And(G[i][j].Equals(model[G[i][j]]) for i in range(N) for j in range(N))
            )
            if solver.solve():
                print("The solution is not unique!")
                print_sol(solver.get_model())
            else:
                print("The solution is unique!")
        else:
            print("UNSAT")


if __name__ == "__main__":
    main()
