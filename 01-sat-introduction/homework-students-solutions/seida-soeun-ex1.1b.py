from z3 import *

s = Solver()

# (x1 -> x2 ) ∨ x3 === (-x1 ∨ x2 ) ∨ x3 === -x1 ∨ x2 ∨ x3
# -1 2 3 0   ->   Or(Not(x1), x2, x3)

x1, x2, x3 = Bools('x1 x2 x3')

s.add(
    Or(Not(x1), x2, x3)
)

result = s.check()

if result == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")
