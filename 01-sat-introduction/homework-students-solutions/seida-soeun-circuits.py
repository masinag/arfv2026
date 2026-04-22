from z3 import *

s = Solver()

# x1 <-> a && b
# x2 <-> b || c
# x3 <-> b && c
# x4 <-> x2 && x3
# o1 <-> x1 || x4
# x5 <-> a || c
# o2 <-> x5 && b
# !(o1 <-> o2)

a, b, c = Bools('a b c')
x1, x2, x3, x4, o1, x5, o2 = Bools('x1 x2 x3 x4 o1 x5 o2')

s.add(
    And(
        # x1 <-> a && b
        Or(Not(x1), a),
        Or(Not(x1), b),
        Or(x1, Not(a), Not(b)),

        # x2 <-> b || c
        Or(Not(x2), b, c),
        Or(x2, Not(b)),
        Or(x2, Not(c)),

        # x3 <-> b && c
        Or(Not(x3), b),
        Or(Not(x3), c),
        Or(x3, Not(b), Not(c)),

        # x4 <-> x2 && x3
        Or(Not(x4), x2),
        Or(Not(x4), x3),
        Or(x4, Not(x2), Not(x3)),

        # o1 <-> x1 || x4
        Or(Not(o1), x1, x4),
        Or(o1, Not(x1)),
        Or(o1, Not(x4)),

        # x5 <-> a || c
        Or(Not(x5), a, c),
        Or(x5, Not(a)),
        Or(x5, Not(c)),

        # o2 <-> x5 && b
        Or(Not(o2), x5),
        Or(Not(o2), b),
        Or(o2, Not(x5), Not(b)),

        # !(o1 <-> o2)
        Or(o1, o2),
        Or(Not(o1), Not(o2))
    )
)

result = s.check()

if result == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")