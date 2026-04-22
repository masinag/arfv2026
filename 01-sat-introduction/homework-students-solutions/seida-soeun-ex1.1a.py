from z3 import *

s = Solver()

# 1  -5  4  0   ->   Or(x1, Not(x5), x4)
# -3  4  0      ->   Or(Not(x3), x4)
# -1  5  2  0   ->   Or(Not(x1), x5, x2)

x1, x2, x3, x4, x5 = Bools('x1 x2 x3 x4 x5')

s.add(
    And(
        Or(x1, Not(x5), x4),
        Or(Not(x3), x4),
        Or(Not(x1), x5, x2)
    )
)

result = s.check()

if result == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")
