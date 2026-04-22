from z3 import *

s = Solver()

# pXY = digit Y is in position X
p11, p12, p13, p14 = Bools('p11 p12 p13 p14')
p21, p22, p23, p24 = Bools('p21 p22 p23 p24')
p31, p32, p33, p34 = Bools('p31 p32 p33 p34')

# The password should be even
s.add(Xor(p32, p34))

# We cannot use the same digit three times
s.add(
    And(
        Or(Not(p11), Not(p21), Not(p31)),
        Or(Not(p12), Not(p22), Not(p32)),
        Or(Not(p13), Not(p23), Not(p33)),
        Or(Not(p14), Not(p24), Not(p34))
    )
)

# Repeating the same digit twice is allowed, but not in adjacent positions
s.add(Implies(p21, And(Not(p11), Not(p31))))
s.add(Implies(p22, And(Not(p12), Not(p32))))
s.add(Implies(p23, And(Not(p13), Not(p33))))
s.add(Implies(p24, And(Not(p14), Not(p34))))

# Hidden condition: at least one digit per position
s.add(
    And(
        Or(p11, p12, p13, p14),
        Or(p21, p22, p23, p24),
        Or(p31, p32, p33, p34)
    )
)

# At most one digit per position
s.add(
    And(
        Implies(p11, Not(Or(p12, p13, p14))),
        Implies(p12, Not(Or(p11, p13, p14))),
        Implies(p13, Not(Or(p11, p12, p14))),
        Implies(p14, Not(Or(p11, p12, p13)))
    )
)

s.add(
    And(
        Implies(p21, Not(Or(p22, p23, p24))),
        Implies(p22, Not(Or(p21, p23, p24))),
        Implies(p23, Not(Or(p21, p22, p24))),
        Implies(p24, Not(Or(p21, p22, p23)))
    )
)

s.add(
    And(
        Implies(p31, Not(Or(p32, p33, p34))),
        Implies(p32, Not(Or(p31, p33, p34))),
        Implies(p33, Not(Or(p31, p32, p34))),
        Implies(p34, Not(Or(p31, p32, p33)))
    )
)

# Check whether 434 is unique by blocking that solution
s.add(Or(Not(p14), Not(p23), Not(p34)))

result = s.check()

if result == sat:
    print("SATISFIABLE")
    m = s.model()
    vars_ = [
        p11, p12, p13, p14,
        p21, p22, p23, p24,
        p31, p32, p33, p34
    ]
    for v in vars_:
        print(f"{v} = {m[v]}")

    # Decode password
    pos1 = next(d for d, v in [(1, p11), (2, p12), (3, p13), (4, p14)] if is_true(m[v]))
    pos2 = next(d for d, v in [(1, p21), (2, p22), (3, p23), (4, p24)] if is_true(m[v]))
    pos3 = next(d for d, v in [(1, p31), (2, p32), (3, p33), (4, p34)] if is_true(m[v]))

    print("Model:", f"{pos1}{pos2}{pos3}")
else:
    print("UNSATISFIABLE")