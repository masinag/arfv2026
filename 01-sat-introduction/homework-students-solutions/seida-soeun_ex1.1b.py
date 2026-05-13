from z3 import *

s = Solver()

# (x1 -> x2 ) ∨ x3 === (-x1 ∨ x2 ) ∨ x3 === -x1 ∨ x2 ∨ x3

x1, x2, x3 = Bools('x1 x2 x3')

s.add(
    Or(
        Implies(x1, x2), x3
    )  # (x1 -> x2 ) ∨ x3
)

# s.add(
#     Or(
#         Or(Not(x1), x2),
#         x3)  # (-x1 ∨ x2 ) ∨ x3
# )

# s.add(
#     Or(Not(x1), x2, x3) # -x1 ∨ x2 ∨ x3
# )

result = s.check()

if result == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")
