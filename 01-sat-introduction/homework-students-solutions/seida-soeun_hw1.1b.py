from z3 import *

s = Solver()

# x1 <-> x2 === (-x1 v x2) and (x1 v -x2)
x1, x2 = Bools('x1 x2')

# s.add(x1 == x2) # x1 <-> x2

s.add(
    And(
        Or(Not(x1), x2),
        Or(x1, Not(x2))
    )
) # (-x1 v x2) and (x1 v -x2)

if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")
