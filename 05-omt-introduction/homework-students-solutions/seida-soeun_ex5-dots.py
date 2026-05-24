from z3 import *

s = Solver()

# Use MathSAT to solve the puzzle shown in
# the figure. The rules are simple: you must
# connect dots with the same color with a
# single line and all cells must be used to
# generate a valid solution.

red = 1
green = 2
blue = 3
yellow = 4

grid = {
    (row, column): Int(f"row{row}column{column}")
    for row in range(1, 6)
    for column in range(1, 6)
}

colors = [red, green, blue, yellow]

# constrain
constrain = {
    red: [(1, 1), (5, 4)],
    green: [(4, 2), (5, 5)],
    blue: [(3, 2), (2, 4)],
    yellow: [(1, 2), (3, 3)]
}

for color in colors:
    for row, column in constrain[color]:
        s.add(
            grid[(row, column)] == color
        )

# one cell, one color
for row in range(1, 6):
    for column in range(1, 6):
        s.add(
            Or(*[grid[(row, column)] == color for color in colors]),
            AtMost(*[grid[(row, column)] == color for color in colors], 1)
        )

# fill the possible color
for color in colors:
    for row in range(1, 6):
        for column in range(1, 6):
            neighbor = []
            if row > 1:
                neighbor.append(grid[(row - 1, column)] == color) # up
            if row < 5:
                neighbor.append(grid[(row + 1, column)] == color) # down
            if column > 1:
                neighbor.append(grid[(row, column - 1)] == color) # left
            if column < 5:
                neighbor.append(grid[(row, column + 1)] == color) # right
            count = Sum([If(x, 1, 0) for x in neighbor])

            if (row, column) in constrain[color]:
                s.add(
                    count == 1
                )
            else:
                s.add(
                    Implies(
                        grid[(row, column)] == color,
                        count == 2
                    )
                )
if s.check() == sat:
    print("satisfiable")
    model = s.model()
    for row in range(1, 6):
        for column in range(1, 6):
            value = model.evaluate(grid[(row, column)])

            if value.as_long() == red:
                print("Red", end=" ")
            elif value.as_long() == green:
                print("Green", end=" ")
            elif value.as_long() == blue:
                print("Blue", end=" ")
            elif value.as_long() == yellow:
                print("Yellow", end=" ")
        print()
else:
    print("unsatisfiable")