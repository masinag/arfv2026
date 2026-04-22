from z3 import *

s = Solver()

x1, x2 = Bools('x1 x2')

s.add(
    And(
        Or(Not(x1), x2),
        Or(x1, Not(x2))
    )
)

if s.check() == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")
