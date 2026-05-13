from z3 import *

s = Solver()

# color-node
ca, cb, cc, cd = Bools("ca cb cc cd")

# You are given the graph shown in the figure on the
# right. Suppose you want to color the nodes of this
# graph so that nodes connected by an edge cannot
# have the same color. Given these assumptions:
# - Is it possible to color the graph using only 2
# colors?
# Solve it using a SAT solver.

# a -> b
# | \  |
# d -> c

# nodes connected by an edge cannot have the same color (true = x-color, false = y-color)
s.add(
    Xor(ca, cb),
    Xor(ca, cc),
    Xor(ca, cd),
    Xor(cc, cd),
    Xor(cc, cb)
)

if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")