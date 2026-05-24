from z3 import *

s = Solver()

# A, B, C, and D are distinct single-digit numbers. Solve the following equations :
# a + c = d
# a * b = c
# c - b = b
# a * 4 = d

a = Int("a")
b = Int("b")
c = Int("c")
d = Int("d")


def is_digit(number):
    return And(number >= 0, number < 10)


s.add(
    is_digit(a), is_digit(b), is_digit(c), is_digit(d)
)
s.add(
    Distinct(a, b, c, d)
)

# a + c = d
s.add(a + c == d)
# a * b = c
s.add(a * b == c)
# c - b = b
s.add(c - b == b)
# a * 4 = d
s.add(a * 4 == d)

if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")

s.add(Or(
    And(
        d != 8,
        c != 6,
        b != 3,
        a != 2
    )
))
if s.check() == unsat:
    print("unique")
else:
    print("not unique")
    print("second model", s.model())
