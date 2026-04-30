from z3 import *

s = Solver()

in11, in12, in13, in14 = Bools("in11 in12 in13 in14")
in21, in22, in23, in24 = Bools("in21 in22 in23 in24")

# You have to guess a two digits code, with digits from 1 to 4. You have three hints:
# - In12, one number is correct and well placed.
# - In14, nothing is correct.
# - In43, one number is correct but wrongly placed.
# Does a solution exist? Is it unique?

# In12, one number is correct and well placed.
s.add(
    Xor(
        And(in11, Not(Or(in12, in13, in14))),
        And(in22, Not(Or(in21, in23, in24)))
    )
)

# In14, nothing is correct.
s.add(
    Not(in11),
    Not(in21),
    Not(in14),
    Not(in24)
)

# In43, one number is correct but wrongly placed.
s.add(
    Or(in13, in24),
    AtMost(in13, in24, 1)
)

# one number must has a place
s.add(
    Or(in11, in12, in13, in14), # one digit possible
    AtMost(in11, in12, in13, in14, 1), # only one number in a place
    Or(in21, in22, in23, in24),
    AtMost(in21, in22, in23, in24, 1)
)

# find a unique, there is exactly one possible 2-digit code that satisfies all the hints or only 1 solution is satisfies
if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("model: ", model)

    # or (vars != is_true), are there any possible result that differ from the previous result of the var(...)
    s.add(
        Or([
            var != is_true(model.evaluate(var, model_completion=True))
            for var in [in11, in12, in13, in14, in21, in22, in23, in24]
        ])
    )
    if s.check() == sat:
        print("not unique")
        print("second model:", s.model())
    else:
        print("unique")
else:
    print("unsatisfiable")
