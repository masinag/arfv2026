from z3 import *

s = Solver()

# Homework 2.4: The N-Queens Problem
# The N-queens problem is to place N queens on an N×N chess board such that no two
# queens are mutually attacking(i.e., in the same row, column, or diagonal).
# - Solve the N-queens problem with N = 8.
# - Is the solution obtained unique?

# queen = 8 so set 8 true on board to show the place of each queen

board = {
    (row, column): Bool(f"row{row}column{column}")
    for row in range(1, 9)
    for column in range(1, 9)
}

# one row, one queen
for row in range(1, 9):
    s.add(
        AtMost(*[board[row, column] for column in range(1, 9)], 1),
        Or(*[board[row, column] for column in range(1, 9)])
    )

# one column, one queen
for column in range(1, 9):
    s.add(
        AtMost(*[board[row, column] for row in range(1, 9)], 1),
        Or(*[board[row, column] for row in range(1, 9)])
    )

# one diagonal, one queen
for row in range(1, 9):
    for column in range(1, 9):
        for row2 in range(1, 9):
            for column2 in range(1, 9):
                # skip the queen place
                if row == row2 and column == column2:
                    continue
                if abs(row - row2) == abs(column - column2):
                    s.add(
                        Or(
                            Not(board[row, column]),
                            Not(board[row2, column2])
                        )
                    )
if s.check() == sat:
    print("satisfiable")
    model = s.model()
    second_model = []
    for row in range(1, 9):
        for column in range(1, 9):
            valid = is_true(model.evaluate(board[row, column], model_completion=True))
            second_model.append(board[row, column] != valid)
            # print(model.evaluate(board[row, column]), end=" ")
            if valid:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    s.add(Or(second_model))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        print("second model:", s.model())
else:
    print("unsatisfiable")
