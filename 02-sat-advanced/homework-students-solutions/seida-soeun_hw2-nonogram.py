from z3 import *

s = Solver()

#     | 2 3 4 2 2
# -------------
#   2 | 0 0 0 0 0
#   3 | 0 0 0 0 0
#   3 | 0 0 0 0 0
# 3 1 | 0 0 0 0 0
#   1 | 0 0 0 0 0

# true for black, false for x

grid = {
    (row, column): Bool(f"row{row}column{column}")
    for row in range(1, 6)
    for column in range(1, 6)
}

# constraint
s.add(
    Or(
        And(grid[1, 1], grid[1, 2], Not(grid[1, 3]), Not(grid[1, 4]), Not(grid[1, 5])),
        And(Not(grid[1, 1]), grid[1, 2], grid[1, 3], Not(grid[1, 4]), Not(grid[1, 5])),
        And(Not(grid[1, 1]), Not(grid[1, 2]), grid[1, 3], grid[1, 4], Not(grid[1, 5])),
        And(Not(grid[1, 1]), Not(grid[1, 2]), Not(grid[1, 3]), grid[1, 4], grid[1, 5])
    )
)
s.add(
    Or(
        And(grid[2, 1], grid[2, 2], grid[2, 3], Not(grid[2, 4]), Not(grid[2, 5])),
        And(Not(grid[2, 1]), grid[2, 2], grid[2, 3], grid[2, 4], Not(grid[2, 5])),
        And(Not(grid[2, 1]), Not(grid[2, 2]), grid[2, 3], grid[2, 4], grid[2, 5])
    )
)

s.add(
    Or(
        And(grid[3, 1], grid[3, 2], grid[3, 3], Not(grid[3, 4]), Not(grid[3, 5])),
        And(Not(grid[3, 1]), grid[3, 2], grid[3, 3], grid[3, 4], Not(grid[3, 5])),
        And(Not(grid[3, 1]), Not(grid[3, 2]), grid[3, 3], grid[3, 4], grid[3, 5])
    )
)

s.add(And(grid[4, 1], grid[4, 2], grid[4, 3], Not(grid[4, 4]), grid[4, 5]))

s.add(
    Or(
        And(grid[5, 1], Not(grid[5, 2]), Not(grid[5, 3]), Not(grid[5, 4]), Not(grid[5, 5])),
        And(Not(grid[5, 1]), grid[5, 2], Not(grid[5, 3]), Not(grid[5, 4]), Not(grid[5, 5])),
        And(Not(grid[5, 1]), Not(grid[5, 2]), grid[5, 3], Not(grid[5, 4]), Not(grid[5, 5])),
        And(Not(grid[5, 1]), Not(grid[5, 2]), Not(grid[5, 3]), grid[5, 4], Not(grid[5, 5])),
        And(Not(grid[5, 1]), Not(grid[5, 2]), Not(grid[5, 3]), Not(grid[5, 4]), grid[5, 5])
    )
)

s.add(
    Or(
        And(grid[1, 1], grid[2, 1], Not(grid[3, 1]), Not(grid[4, 1]), Not(grid[5, 1])),
        And(Not(grid[1, 1]), grid[2, 1], grid[3, 1], Not(grid[4, 1]), Not(grid[5, 1])),
        And(Not(grid[1, 1]), Not(grid[2, 1]), grid[3, 1], grid[4, 1], Not(grid[5, 1])),
        And(Not(grid[1, 1]), Not(grid[2, 1]), Not(grid[3, 1]), grid[4, 1], grid[5, 1])
    )
)

s.add(
    Or(
        And(grid[1, 2], grid[2, 2], grid[3, 2], Not(grid[4, 2]), Not(grid[5, 2])),
        And(Not(grid[1, 2]), grid[2, 2], grid[3, 2], grid[4, 2], Not(grid[5, 2])),
        And(Not(grid[1, 2]), Not(grid[2, 2]), grid[3, 2], grid[4, 2], grid[5, 2])
    )
)

s.add(
    Or(
        And(grid[1, 3], grid[2, 3], grid[3, 3], grid[4, 3], Not(grid[5, 3])),
        And(Not(grid[1, 3]), grid[2, 3], grid[3, 3], grid[4, 3], grid[5, 3]),
    )
)

s.add(
    Or(
        And(grid[1, 4], grid[2, 4], Not(grid[3, 4]), Not(grid[4, 4]), Not(grid[5, 4])),
        And(Not(grid[1, 4]), grid[2, 4], grid[3, 4], Not(grid[4, 4]), Not(grid[5, 4])),
        And(Not(grid[1, 4]), Not(grid[2, 4]), grid[3, 4], grid[4, 4], Not(grid[5, 4])),
        And(Not(grid[1, 4]), Not(grid[2, 4]), Not(grid[3, 4]), grid[4, 4], grid[5, 4])
    )
)

s.add(
    Or(
        And(grid[1, 5], grid[2, 5], Not(grid[3, 5]), Not(grid[4, 5]), Not(grid[5, 5])),
        And(Not(grid[1, 5]), grid[2, 5], grid[3, 5], Not(grid[4, 5]), Not(grid[5, 5])),
        And(Not(grid[1, 5]), Not(grid[2, 5]), grid[3, 5], grid[4, 5], Not(grid[5, 5])),
        And(Not(grid[1, 5]), Not(grid[2, 5]), Not(grid[3, 5]), grid[4, 5], grid[5, 5])
    )
)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    second_model = []
    for row in range(1, 6):
        row_value = []
        for column in range(1, 6):
            value = is_true(model.evaluate(grid[row, column]))
            row_value.append(value)
            print("b" if value else "x", end=" ")
        second_model.append(row_value)
        print()
    second_grid = []
    for row in range(1, 6):
        for column in range(1, 6):
            # suppose first_model[0][0] == False then is grid[1, 1] != False?
            second_grid.append(grid[row, column] != second_model[row -1][column -1])
    s.add(Or(second_grid))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        print("second model: ", s.model())
else:
    print("unsatisfiable")
