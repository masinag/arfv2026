from z3 import *

s = Solver()

# xij = number i is in position j
x11, x12 = Bools("x11 x12")
x21, x22 = Bools("x21 x22")
x31, x32 = Bools("x31 x32")
x41, x42 = Bools("x41 x42")

# In 12, one number is correct and well placed
s.add(
    Or(
        And(x11, Not(x21), Not(x22)),
        And(x22, Not(x11), Not(x12))
    )
)

# In 14, nothing is correct
s.add(
    And(
        Not(x11), Not(x12),
        Not(x41), Not(x42)
    )
)

# In 43, one number is correct but wrongly placed
s.add(
    Or(
        And(x31, Not(x41), Not(x42)),
        And(x42, Not(x31), Not(x32))
    )
)

# Hidden condition: each position must contain exactly one number
s.add(Or(x11, x21, x31, x41))
s.add(Or(x12, x22, x32, x42))

s.add(
    And(
        Implies(x11, And(Not(x21), Not(x31), Not(x41))),
        Implies(x21, And(Not(x11), Not(x31), Not(x41))),
        Implies(x31, And(Not(x11), Not(x21), Not(x41))),
        Implies(x41, And(Not(x11), Not(x21), Not(x31))),

        Implies(x12, And(Not(x22), Not(x32), Not(x42))),
        Implies(x22, And(Not(x12), Not(x32), Not(x42))),
        Implies(x32, And(Not(x12), Not(x22), Not(x42))),
        Implies(x42, And(Not(x12), Not(x22), Not(x32)))
    )
)

result = s.check()

if result == sat:
    print("SATISFIABLE")
    m = s.model()
    vars_ = [x11, x12, x21, x22, x31, x32, x41, x42]
    for v in vars_:
        print(f"{v} = {m[v]}")

    # decode the 2-digit code
    pos1 = None
    pos2 = None
    for digit, var in [(1, x11), (2, x21), (3, x31), (4, x41)]:
        if is_true(m[var]):
            pos1 = digit
    for digit, var in [(1, x12), (2, x22), (3, x32), (4, x42)]:
        if is_true(m[var]):
            pos2 = digit

    print("Model:", pos1, pos2)
else:
    print("UNSATISFIABLE")