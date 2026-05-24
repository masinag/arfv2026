from z3 import *


# Solve it using an SMT solver
# (hint: use temporary variables
# to store intermediate results)
# Questions:
# 1. What type should the
# variables have?
# 2. What happens if instead
# we impose the sum to be
# equal to 58?

results = [56, 58]

def solve(final_result):
    yellow, red, green, blue = Reals("yellow red green blue")
    s = Solver()

    first = green + blue
    second = 2 * red
    left = (2 * yellow) + first + second

    third = (3 * yellow) + green
    fourth = green + red
    right = third + fourth

    # balance
    s.add(
        first == second,
        third == fourth,
        right == left
    )
    # total
    s.add(
        right + left == final_result
    )
    for color in [yellow, red, green, blue]:
        s.add(color > 0)
    print("total:", final_result)
    if s.check() == sat:
        model = s.model()
        print("satisfiable")
        print(f"red: {model[red]}, green: {model[green]}, blue: {model[blue]}, yellow: {model[yellow]}")
    else:
        print("unsatisfiable")
for result in results:
    solve(result)

# 1, variables should be ints if the weights could be only decimals number
# 2, if total = 58, the integer version is unsatisfiable so can change to real to make it satisfiable by allows a fractional solution
