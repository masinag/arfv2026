from z3 import *

s = Solver()

# Kakuro is a puzzle in which one must put the
# numbers 1 to 9 in the different cells such that they
# satisfy certain constraints.
# If a clue is present in a row or column, the sum of
# the cell for that row should be equal to the value.
# Within each sum all the numbers have to be
# different, so to add up to 4 we can have 1+3 or 3+1.
# Can we find a solution using SMT solvers?

grid = {
    (row, column): Int(f"row{row}column{column}")
    for row in range(1, 7)
    for column in range(1, 6)
}

block_cells = [
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
    (2, 1), (2, 5),
    (3, 1), (3, 5),
    (4, 1), (4, 4), (4, 5),
    (5, 1), (5, 2),
    (6, 1), (6, 2)
]

# set block cell which cannot fill to 0
for cell in block_cells:
    s.add(
        grid[cell] == 0
    )

# possible number only 1-9
for row in range(1, 7):
    for column in range(1, 6):
        if (row, column) not in block_cells:
            s.add(
                grid[row, column] > 0, grid[row, column] <= 9
            )

# condition
s.add(
    grid[2, 2] + grid[2, 3] + grid[2, 4] == 9,
    Distinct(grid[2, 2], grid[2, 3], grid[2, 4]),
    grid[3, 2] + grid[3, 3] + grid[3, 4] == 13,
    Distinct(grid[3, 2], grid[3, 3], grid[3, 4]),
    grid[4, 2] + grid[4, 3] == 13,
    Distinct(grid[4, 2], grid[4, 3]),
    grid[5, 3] + grid[5, 4] + grid[5, 5] == 7,
    Distinct(grid[5, 3], grid[5, 4], grid[5, 5]),
    grid[6, 3] + grid[6, 4] + grid[6, 5] == 19,
    Distinct(grid[6, 3], grid[6, 4], grid[6, 5]),

    grid[2, 2] + grid[3, 2] + grid[4, 2] == 9,
    Distinct(grid[2, 2], grid[3, 2], grid[4, 2]),
    grid[2, 3] + grid[3, 3] + grid[4, 3] + grid[5, 3] + grid[6, 3] == 34,
    Distinct(grid[2, 3], grid[3, 3], grid[4, 3], grid[5, 3], grid[6, 3]),
    grid[2, 4] + grid[3, 4] == 4,
    Distinct(grid[2, 4], grid[3, 4]),
    grid[5, 4] + grid[6, 4] == 11,
    Distinct(grid[5, 4], grid[6, 4]),
    grid[5, 5] + grid[6, 5] == 3,
    Distinct(grid[5, 5], grid[6, 5])
)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    for row in range(1, 7):
        for column in range(1, 6):
            print(model.evaluate(grid[row, column]), end=" ")
        print()
else:
    print("unsatisfiable")