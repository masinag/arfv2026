from pysmt.shortcuts import BOOL, And, Solver, Symbol, ExactlyOne

SIZE = 9
nn = list(range(1, SIZE + 1))

xx = {f"x_{i}_{j}_{k}": Symbol(f"x_{i}_{j}_{k}", BOOL) for i in nn for j in nn for k in nn}


def print_solution(model):
    for row in nn:
        for col in nn:
            number = [num for num in nn if model[xx[f"x_{row}_{col}_{num}"]].is_true()]
            assert len(number) == 1, (number, row, col)
            number = number[0]
            print(number, end=" ")
        print()


assertions = []

# Sudoku rules:
# Every number is contained exactly once in every row
for number in nn:
    for row in nn:
        assertions.append(ExactlyOne(xx[f"x_{row}_{col}_{number}"] for col in nn))

# Every number is contained exactly once in every column
for number in nn:
    for col in nn:
        assertions.append(ExactlyOne(xx[f"x_{row}_{col}_{number}"] for row in nn))

# Every number is contained exactly once in every square
for number in nn:
    for srow in nn[::3]:
        for scol in nn[::3]:
            assertions.append(
                ExactlyOne(
                    xx[f"x_{row}_{col}_{number}"]
                    for row in range(srow, srow + 3)
                    for col in range(scol, scol + 3)
                )
            )

# Every cell contains exactly one number
for row in nn:
    for col in nn:
        assertions.append(ExactlyOne(xx[f"x_{row}_{col}_{number}"] for number in nn))

# Known numbers
assertions.append(
    And(
        xx[f"x_{1}_{4}_{9}"],
        xx[f"x_{1}_{7}_{1}"],
        xx[f"x_{2}_{8}_{3}"],
        xx[f"x_{2}_{9}_{5}"],
        xx[f"x_{3}_{3}_{8}"],
        xx[f"x_{3}_{5}_{7}"],
        xx[f"x_{4}_{5}_{5}"],
        xx[f"x_{4}_{7}_{9}"],
        xx[f"x_{5}_{1}_{1}"],
        xx[f"x_{5}_{3}_{4}"],
        xx[f"x_{5}_{4}_{3}"],
        xx[f"x_{5}_{7}_{2}"],
        xx[f"x_{6}_{2}_{7}"],
        xx[f"x_{6}_{6}_{9}"],
        xx[f"x_{6}_{9}_{3}"],
        xx[f"x_{7}_{3}_{5}"],
        xx[f"x_{7}_{5}_{2}"],
        xx[f"x_{7}_{6}_{7}"],
        xx[f"x_{8}_{2}_{4}"],
        xx[f"x_{8}_{3}_{9}"],
        xx[f"x_{8}_{7}_{8}"],
        xx[f"x_{9}_{1}_{7}"],
        xx[f"x_{9}_{4}_{1}"],
        xx[f"x_{9}_{8}_{2}"],
    )
)


with Solver("msat") as msat:
    msat.add_assertions(assertions)
    if msat.solve():
        print("Solution found!")
        print_solution(msat.get_model())
    else:
        print("No solution found!")
