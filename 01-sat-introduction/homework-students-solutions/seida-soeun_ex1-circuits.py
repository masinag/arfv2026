from z3 import *

s = Solver()

a, b, c = Bools('a b c')
# (a and b) v ((b v c) and (b and c)) === (a and b) v (b and c) === (a v c) and b, cuz ab + bc = b(a + c)

# s.add(
#     Or(
#         And(a, b),
#         And(Or(b, c), And(b, c)),
#     )
# ) # (a and b) v ((b v c) and (b and c))

# s.add(
#     Or(
#         And(a, b),
#         And(b, c)
#     )
# ) # (a and b) v (b and c)

# s.add(
#     And(
#         b,
#         Or(a, c)
#     )
# ) # (a v c) and b


# check equivalence

original = Or(
    And(a, b),
    And(Or(b, c), And(b, c)),
)

simplified = And(
    b,
    Or(a, c)
)

# goal prove that original and simplified produce the same output for every possible input

# original == simplified, is there at least one case where they are the same?
# but that does not mean they are equivalent for all rows, equivalence means all rows match, not just one row
# 3 variables (2³ = 8 rows)

# original != simplified, let z3 try to find values of a, b, c where the two formulas are different
# so s.check() == unsat mean z3 could not find any case where they are different

s.add(original != simplified)

if s.check() == unsat:
    # print("satisfiable")
    print("equivalent")
else:
    print("not equivalent")
    print("counterexample:", s.model())
