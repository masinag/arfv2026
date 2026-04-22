from z3 import *

s = Solver()

# Two colors: True and False
A, B, C, D = Bools('A B C D')

# A -- B, A -- C, A -- D
s.add(
    And(
        Xor(A, B),
        Xor(A, C),
        Xor(A, D)
    )
)

# B -- C
s.add(Xor(B, C))

# C -- D
s.add(Xor(C, D))

result = s.check()

if result == sat:
    print("SATISFIABLE")
    print("Model:", s.model())
else:
    print("UNSATISFIABLE")