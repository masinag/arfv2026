from z3 import *

s = Solver()

x1, x2 = Bools('x1 x2')

s.add(Or(x1, Not(x1), x2))

if s.check() == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")
