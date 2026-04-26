from z3 import *

s = Solver()

# Consider three chairs in a row and three guests :A,B,C. We know that:
# - A does not want to sit next to C.
# - A does not want to sit on the left most chair.
# - B does not want to sit immediately to the right of C
# Is it possible to satisfy the following constraints and find a valid placement?

a1, a2, a3 = Bools('a1 a2 a3')
b1, b2, b3 = Bools('b1 b2 b3')
c1, c2, c3 = Bools('c1 c2 c3')

# A does not want to sit next to C.
s.add(
    And(
        Not(And(c1, a2)),
        Not(And(c2, a3)),
        Not(And(c3, a2)),
        Not(And(c2, a1)),
    )
)

# A does not want to sit on the left most chair
s.add(Not(a1))

# B does not want to sit immediately to the right of C
s.add(
    And(
        Not(And(c1, b2)),
        Not(And(c2, b3))
    )
)

# each person must have a chair
s.add(
    Or(a1, a2, a3),
    Or(b1, b2, b3),
    Or(c1, c2, c3)
)

# each person sits in one chair only
s.add(
    AtMost(a1, a2, a3, 1),
    AtMost(b1, b2, b3, 1),
    AtMost(c1, c2, c3, 1)
)

# they cannot sit the same chair
s.add(
    AtMost(a1, b1, c1, 1),
    AtMost(a2, b2, c2, 1),
    AtMost(a3, b3, c3, 1)
)

if s.check() == sat:
    print("satisfiable")
    print("model: ",s.model())
else:
    print("unsatisfiable")