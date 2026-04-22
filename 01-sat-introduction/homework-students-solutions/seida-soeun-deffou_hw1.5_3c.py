from z3 import *

s = Solver()

A1, A2, A3 = Bools('A1 A2 A3')
B1, B2, B3 = Bools('B1 B2 B3')
C1, C2, C3 = Bools('C1 C2 C3')
D1, D2, D3 = Bools('D1 D2 D3')

# A -- B
s.add(Not(And(A1, B1)))
s.add(Not(And(A2, B2)))
s.add(Not(And(A3, B3)))

# A -- C
s.add(Not(And(A1, C1)))
s.add(Not(And(A2, C2)))
s.add(Not(And(A3, C3)))

# A -- D
s.add(Not(And(A1, D1)))
s.add(Not(And(A2, D2)))
s.add(Not(And(A3, D3)))

# B -- C
s.add(Not(And(B1, C1)))
s.add(Not(And(B2, C2)))
s.add(Not(And(B3, C3)))

# C -- D
s.add(Not(And(C1, D1)))
s.add(Not(And(C2, D2)))
s.add(Not(And(C3, D3)))

# Hidden conditions (copied exactly from your SMT2)
s.add(Implies(A1, And(Not(A2), Not(A3))))
s.add(Implies(B1, And(Not(B2), Not(B3))))
s.add(Implies(C1, And(Not(C2), Not(C3))))
s.add(Implies(D1, And(Not(D2), Not(D3))))

s.add(
    And(
        Or(A1, A2, A3),
        Or(B1, B3, B3),
        Or(C1, C3, C3),
        Or(D1, D2, D3)
    )
)

result = s.check()

if result == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")