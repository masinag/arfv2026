from z3 import *

s = Solver()

Pippo, Paperino, Topolino, Pluto = Ints("Pippo Paperino Topolino Pluto")
people = [Pippo, Paperino, Topolino, Pluto]

for p in people:
    s.add(And(p >= 1, p <= 4))

s.add(Distinct(people))
s.add(Pippo < Pluto)
s.add(Paperino < Pluto)

if s.check() == sat:
    m = s.model()
    ranking = sorted(
        [(str(p), m[p].as_long()) for p in people],
        key=lambda x: x[1]
    )

    print("SATISFIABLE")
    print("Model:")
    for name, pos in ranking:
        print(f"{pos}: {name}")
else:
    print("UNSATISFIABLE")