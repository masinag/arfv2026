from z3 import *

s = Solver()

# -x1 -> (x1 -> x2) === x1 v (-x1 v x2) === x1 v -x1 v x2
x1, x2 = Bools('x1 x2')

s.add(
    Implies(Not(x1),
        Implies(x1, x2)
        )
) # -x1 -> (x1 -> x2)

# s.add(
#     Or(
#         x1, Or(Not(x1), x2),
#     )
# ) # x1 v (-x1 v x2)

# s.add(
#     Or(x1, Not(x1), x2)
# ) # x1 v -x1 v x2

if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")
