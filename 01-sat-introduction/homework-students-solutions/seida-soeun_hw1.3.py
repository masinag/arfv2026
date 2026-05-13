from z3 import *

s = Solver()

a, b, c = Bools('a b c')

# Three students A, B and C are accused of having illegally obtained the questions for the
# Automated Reasoning exam. During the investigation process the students made the
# following statements:
# - A said: “B is guilty and C is innocent”
# - B said: “If A is guilty, then C is also guilty”
# - C said: “I’m innocent and one of the others,perhaps even the two,are guilty”
# Considering that all the students spoke the truth, which of the students are guilty and
# which are innocent? Solve it using a SAT solver

# A said: “B is guilty and C is innocent”
s.add(
    And(b, Not(c))
)

# B said: “If A is guilty, then C is also guilty”
s.add(
    Implies(a, c)
)

# C said: “I’m innocent and one of the others, perhaps even the two, are guilty”
s.add(
    And(Not(c),
        Or(a, b))
)

# all of them possible are guilty
s.add(
    Or(a, b, c)
)

if s.check() == sat:
    print("satisfiable")
    print("model:", s.model())
else:
    print("unsatisfiable")
