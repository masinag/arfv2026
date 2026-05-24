from z3 import *

s = Solver()

# Exercise 3.3: Mistery Grid
# To solve a MysteryGrid puzzle, place all of the tiles on the grid so that:
#  Every row and every column contains
# exactly one of each type of tile.
# - Cages (regions surrounded by a heavy
# border) have a target and an operation.
# The tiles you place in a cage must make
# the target number using the operation.
# - Inequality clues between cells must be
# respected by the tiles you place.
# - Tiles with a lock are already placed on
# the grid and cannot be moved

tiles = {
    "orange": 7,
    "red": 2,
    "yellow": 3
}
grid = {
    (row, column): Real(f"row{row}column{column}")
    for row in range(1, 4)
    for column in range(1, 4)
}

# constrain
s.add(
    grid[1, 3] == tiles["orange"],
    grid[3, 2] + grid[3, 3] == 5,
    grid[1, 1] + grid[2, 1] + grid[3, 1] == 12,
    grid[1, 1] < grid[2, 1],
    grid[1, 2] * grid[2, 2] * grid[2, 3] == 42
)

#  Every row and every column contains exactly one of each type of tile.
for row in range(1, 4):
    s.add(
        Distinct(*[grid[row, column] for column in range(1, 4)])
    )
for column in range(1, 4):
    s.add(
        Distinct(*[grid[row, column] for row in range(1, 4)])
    )

# one grid, one tile
for row in range(1, 4):
    for column in range(1, 4):
        s.add(
            Or(
                *[grid[row, column] == tiles[tile] for tile in tiles]
            ),
            AtMost(
                *[grid[row, column] == tiles[tile] for tile in tiles], 1
            )
        )

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    grid_second = []
    for row in range(1, 4):
        for column in range(1, 4):
            valid = model.evaluate(grid[row, column], model_completion=True)
            grid_second.append(grid[row, column] != valid)
            print(model[grid[row, column]], end=" ")
        print()
    s.add(Or(grid_second))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        print("second model:", s.model())
else:
    print("unsatisfiable")