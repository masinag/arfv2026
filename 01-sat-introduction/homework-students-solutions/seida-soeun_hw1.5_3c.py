from z3 import *

s = Solver()

# color-node-color-x
ca1, ca2, ca3 = Bools("ca1 ca2 ca3")
cb1, cb2, cb3 = Bools("cb1 cb2 cb3")
cc1, cc2, cc3 = Bools("cc1 cc2 cc3")
cd1, cd2, cd3 = Bools("cd1 cd2 cd3")

# You are given the graph shown in the figure on the
# right. Suppose you want to color the nodes of this
# graph so that nodes connected by an edge cannot
# have the same color. Given these assumptions:
# - Is it possible to color the graph using only 3
# colors?
# Solve it using a SAT solver.

# a -> b
# | \  |
# d -> c

# one node, one color and a node possible colored
s.add(
    AtMost(ca1, ca2, ca3, 1),
    Or(ca1, ca2, ca3),
    AtMost(cb1, cb2, cb3, 1),
    Or(cb1, cb2, cb3),
    AtMost(cc1, cc2, cc3, 1),
    Or(cc1, cc2, cc3),
    AtMost(cd1, cd2, cd3, 1),
    Or(cd1, cd2, cd3)
)

# nodes connected by an edge cannot have the same color
s.add(
    Not(And(ca1, cd1)), # ad
    Not(And(ca2, cd2)),
    Not(And(ca3, cd3)),
    Not(And(ca1, cb1)), # ab
    Not(And(ca2, cb2)),
    Not(And(ca3, cb3)),
    Not(And(ca1, cc1)), # ac
    Not(And(ca2, cc2)),
    Not(And(ca3, cc3)),
    Not(And(cc1, cb1)), # cb
    Not(And(cc2, cb2)),
    Not(And(cc3, cb3)),
    Not(And(cc1, cd1)), # cd
    Not(And(cc2, cd2)),
    Not(And(cc3, cd3)),
)


if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")