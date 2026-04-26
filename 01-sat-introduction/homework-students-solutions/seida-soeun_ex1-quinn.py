from z3 import *

s = Solver()

# the formula must be in CNF: (l11 ∨ l12 ∨ ...) ∧ (l21 ∨ l22 ∨ ...) ∧ ... and each clause is terminated by a 0
# p cnf 7 8  -> 7 variables, 8 clauses

x1, x2, x3, x4, x5, x6, x7 = Bools('x1 x2 x3 x4 x5 x6 x7')

s.add(
    And(
        Or(x1, x2), #  1   2 0
        Or(Not(x2), Not(x4)), # -2  -4 0
        Or(x3, x4), #  3   4 0
        Or(Not(x4), Not(x5)), # -4  -5 0
        Or(x5, Not(x6)), #  5  -6 0
        Or(x6, Not(x7)), #  6  -7 0
        Or(x6, x7), #  6   7 0
        Or(x7, Not(x3)) #  7  -3 0
    )
)

if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")







