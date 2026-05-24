from z3 import *

s = Optimize()

# Given an undirected graph, a clique is a subset of vertices such
# that every two distinct vertices in the clique are adjacent.
# Find the maximum clique of this graph using OptiMathSAT.

a, b, c, d = Bools('a b c d')

size = Sum([
    If(a, 1, 0),
    If(b, 1, 0),
    If(c, 1, 0),
    If(d, 1, 0),
])

# b d, not connect
s.add(Not(And(b, d)))

s.maximize(size)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("max size:", model.evaluate(size))
    print("clique:")
    if is_true(model.evaluate(a)):
        print("a")
    if is_true(model.evaluate(b)):
        print("b")
    if is_true(model.evaluate(c)):
        print("c")
    if is_true(model.evaluate(d)):
        print("d")
else:
    print("unsatisfiable")

