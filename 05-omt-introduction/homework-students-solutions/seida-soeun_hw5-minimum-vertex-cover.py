from z3 import *

s = Optimize()

# A vertex-cover set of an undirected graph
# is a subset of vertices such that if an edge
# belongs to the graph, then at least one
# of the two nodes linked by this edge
# belongs to the vertex-cover set.
# Use OptiMathSAT to compute the
# vertex-cover of the minimum size of the
# graph in the figure.
# Try to encode it using both OMT and
# MaxSMT

a, b, c, d, e, f, g = Bools('a b c d e f g')

size = Sum([
    If(a, 1, 0),
    If(b, 1, 0),
    If(c, 1, 0),
    If(d, 1, 0),
    If(e, 1, 0),
    If(f, 1, 0),
    If(g, 1, 0)
])

# connected
s.add(Or(a, b))
s.add(Or(b, c))
s.add(Or(c, e))
s.add(Or(c, d))
s.add(Or(e, d))
s.add(Or(d, f))
s.add(Or(e, f))
s.add(Or(d, g))

s.minimize(size)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("minimum size:", model.evaluate(size))

    for name, var in [("a", a), ("b", b), ("c", c), ("d", d), ("e", e), ("f", f), ("g", g)]:
        if is_true(model.evaluate(var, model_completion=True)):
            print(name)
else:
    print("unsatisfiable")