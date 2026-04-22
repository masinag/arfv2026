from z3 import *

s = Solver()

# students: True = guilty, False = innocent
A, B, C = Bools('A B C')

# A said: "B is guilty and C is innocent"
s.add(And(B, Not(C)))

# B said: "if A is guilty, then C is also guilty"
s.add(Implies(A, C))

# C said: "I'm innocent and one of the others, perhaps even the two, are guilty"
s.add(And(Not(C), Or(A, B)))

# B is guilty
s.add(B)

result = s.check()

if result == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")