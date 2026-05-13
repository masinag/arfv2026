from z3 import *

s = Solver()

x1, x2, x3, x4, x5 = Bools('x1 x2 x3 x4 x5')

# (x1 ∨ -x5 ∨ x4) ∧ (-x3 ∨ x4) ∧ (-x1 ∨ x5 ∨ x2)
s.add(
    And(
        Or(x1, Not(x5), x4), # (x1 ∨ -x5 ∨ x4)
        Or(Not(x3), x4), # (-x3 ∨ x4)
        Or(Not(x1), x5, x2) # (-x1 ∨ x5 ∨ x2)
    )
)

result = s.check()

if result == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")
