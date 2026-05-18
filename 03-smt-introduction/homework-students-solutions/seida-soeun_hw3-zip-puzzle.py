from z3 import *

s = Solver()

# You have found a new puzzle
# to solve:
# 1. Draw a line from the first
# dot to the last, moving
# only horizontally or
# vertically.
# 2. Connect the dots in order
# 3. Fill every cell
# 4. You cannot cross the
# walls (the bold lines)
# Use an SMT solver to solve it.

grid = {
    (row, column): Int(f"row{row}column{column}")
    for row in range(1, 5)
    for column in range(1, 5)
}

cells = [
    grid[row, column]
    for row in range(1, 5)
    for column in range(1, 5)
]

# every cell has number 1 to 16
for cell in cells:
    s.add(cell >= 1, cell <= 16)

# fill every cell, no repeated numbers
s.add(Distinct(*cells))

# constrain
s.add(
    grid[2, 2] < grid[4, 1],
    grid[4, 1] < grid[4, 4],
    grid[4, 4] < grid[1, 3],
    grid[1, 3] < grid[1, 4]
)

# not allow cross the walls
walls = [
    ((1, 2), (1, 3)),
    ((2, 2), (2, 3)),
    ((4, 2), (4, 3))
]

def is_wall(r1, c1, r2, c2):
    return ((r1, c1), (r2, c2)) in walls or ((r2, c2), (r1, c1)) in walls

def neighbors(row, column):
    result = []

    if row > 1:
        result.append((row - 1, column))
    if row < 4:
        result.append((row + 1, column))
    if column > 1:
        result.append((row, column - 1))
    if column < 4:
        result.append((row, column + 1))

    return result


for row in range(1, 5):
    for column in range(1, 5):
        possible_next = []

        for r, c in neighbors(row, column):
            if not is_wall(row, column, r, c):
                possible_next.append(grid[r, c] == grid[row, column] + 1)

        s.add(
            Or(
                grid[row, column] == 16,
                Or(possible_next)
            )
        )


if s.check() == sat:
    model = s.model()
    print("satisfiable")
    for row in range(1, 5):
        for column in range(1, 5):
            print(model.evaluate(grid[row, column]), end=" ")
        print()
else:
    print("unsatisfiable")
