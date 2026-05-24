from z3 import *

s = Optimize()

# Solve the color graph problem again with
# the following map of countries (so you must
# ensure adjacent countries do not have the
# same color).
# Use OptiMathSAT to retrieve the minimum
# number of colors that satisfy the problem.

a, b, c, d, e, f, g, h, i, j, k, l = Ints('a b c d e f g h i j k l')
countries = [a, b, c, d, e, f, g, h, i, j, k, l]

color = Int('color')

s.add(color > 0, color <= len(countries))
for country in countries:
    s.add(country > 0, country <= color)

s.add(
    And(
        a != b,
        a != d,
        a != e,
        b != e,
        b != f,
        b != c,
        c != f,
        d != e,
        d != g,
        d != h,
        e != f,
        e != h,
        e != j,
        h != g,
        h != i,
        h != j,
        i != j,
        i != k,
        i != l,
        j != k,
        k != l,
    )
)

s.minimize(color)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("minimum graph colors:", model.evaluate(color))
else:
    print("unsatisfiable")