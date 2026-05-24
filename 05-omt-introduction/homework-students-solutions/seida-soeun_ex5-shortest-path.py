from z3 import *

s = Optimize()

# Use OptiMathSAT to compute the
# shortest path between G and B.

a, b, c, d, e, f, g, h = Ints("a b c d e f g h")

s.add(g == 0)
s.add(Or(a == b + 4, a == d + 2))
s.add(Or(b == a + 4, b == e + 6, b == c + 4))
s.add(Or(c == b + 4, c == e + 7))
s.add(Or(d == a + 2, d == e + 3, d == f + 5))
s.add(Or(e == b + 6, e == c + 7, e == d + 3, e == h + 8))
s.add(Or(f == d + 5, f == g + 9))
s.add(Or(h == g + 3, h == e + 8))

s.minimize(b)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("from g to b:", model.evaluate(b))
else:
    print("unsatisfiable")