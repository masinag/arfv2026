from z3 import *

s = Solver()

# A Diagonal Sudoku has the same rules as a
# classic Sudoku, but the two main diagonals
# must also contain the numbers from 1 to 9.
# Can you find the solution of this Diagonal
# Sudoku using a SAT solver?
# 0 1 2 3 4 5 6 7 8 9
# 1 0 0 5 0 0 0 1 0 0
# 2 0 0 0 4 9 2 0 0 0
# 3 9 0 0 0 0 0 0 0 3
# 4 0 3 0 0 0 0 0 6 0
# 5 0 9 0 0 0 0 0 1 0
# 6 0 2 0 0 0 0 0 7 0
# 7 1 0 0 0 0 0 0 0 8
# 8 0 0 0 6 8 7 0 0 0
# 9 0 0 3 0 0 0 4 0 0

number_row_column = {
    (number, row, column): Bool(f"{number}_{row}_{column}")
    for number in range(1, 10)
    for row in range(1, 10)
    for column in range(1, 10)
}

# one row, one column, one number
for column in range(1, 10):
    for row in range(1, 10):
        s.add(
            AtMost(
                *[number_row_column[number, row, column] for number in range(1, 10)], 1
            ),
            Or(*[number_row_column[number, row, column] for number in range(1, 10)])
        )

# one number, one row
for column in range(1, 10):
    for number in range(1, 10):
        s.add(
            AtMost(
                *[number_row_column[number, row, column] for row in range(1, 10)], 1
            ),
            Or(*[number_row_column[number, row, column] for row in range(1, 10)])
        )

# one number, one column
for row in range(1, 10):
    for number in range(1, 10):
        s.add(
            AtMost(
                *[number_row_column[number, row, column] for column in range(1, 10)], 1
            ),
            Or(*[number_row_column[number, row, column] for column in range(1, 10)])
        )

# first diagonal
for number in range(1, 10):
    s.add(
        AtMost(*[number_row_column[number, i, i] for i in range(1, 10)], 1),
        Or(*[number_row_column[number, i, i] for i in range(1, 10)])
    )

# second diagonal
for number in range(1, 10):
    s.add(
        AtMost(*[number_row_column[number, i, 10 - i] for i in range(1, 10)], 1),
        Or(*[number_row_column[number, i, 10 - i] for i in range(1, 10)])
    )

# 3d unique
for row in [1, 4, 7]:
    for column in [1, 4, 7]:
        for number in range(1, 10):
            s.add(
                AtMost(
                    *[
                        number_row_column[number, r, c]
                        for r in range(row, row + 3)
                        for c in range(column, column + 3)
                    ],
                    1
                ),
                Or(
                    *[
                        number_row_column[number, r, c]
                        for r in range(row, row + 3)
                        for c in range(column, column + 3)
                    ]
                )
            )
s.add(
    And(
        number_row_column[5, 1, 3],
        number_row_column[1, 1, 7],
        number_row_column[4, 2, 4],
        number_row_column[9, 2, 5],
        number_row_column[2, 2, 6],
        number_row_column[9, 3, 1],
        number_row_column[3, 3, 9],
        number_row_column[3, 4, 2],
        number_row_column[6, 4, 8],
        number_row_column[9, 5, 2],
        number_row_column[1, 5, 8],
        number_row_column[2, 6, 2],
        number_row_column[7, 6, 8],
        number_row_column[1, 7, 1],
        number_row_column[8, 7, 9],
        number_row_column[6, 8, 4],
        number_row_column[8, 8, 5],
        number_row_column[7, 8, 6],
        number_row_column[3, 9, 3],
        number_row_column[4, 9, 7]
    )
)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    # print("model: ", model)
    number_row_column_second_model = []
    number_row_column_display = []
    for row in range(1, 10):
        for column in range(1, 10):
            for number in range(1, 10):
                valid = is_true(model.evaluate(number_row_column[number, row, column], model_completion=True))
                if valid:
                    number_row_column_display.append([number, row, column])
                    print(number, end=" ")
                number_row_column_second_model.append(number_row_column[number, row, column] != valid)
        print("")
    s.add(Or(number_row_column_second_model))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        print("second model:", s.model())

else:
    print("unsatisfiable")
