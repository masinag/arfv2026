from z3 import *

s = Solver()

# digit-position
dp11, dp12, dp13 = Bools("dp11 dp12 dp13")
dp21, dp22, dp23 = Bools("dp21 dp22 dp23")
dp31, dp32, dp33 = Bools("dp31 dp32 dp33")
dp41, dp42, dp43 = Bools("dp41 dp42 dp43")

# Using the digits 1, 2, 3 and 4 you need to create a 3-length password. There are some
# rules that must be fulfilled:
# - The password should be even
# - We cannot use the same digit three times, otherwise it would be easy to guess it.
# - It is possible to repeat the same digit twice, just make sure the two digits are not
# adjacent.
# Solve it using a SAT solver and report the solution. Is this unique?


# The password should be even (so the last digit must be 2 or 4)
s.add(
    Or(dp23, dp43)
)

# We cannot use the same digit three times, otherwise it would be easy to guess it.
s.add(
    Not(And(dp11, dp12, dp13)),
    Not(And(dp21, dp22, dp23)),
    Not(And(dp31, dp32, dp33)),
    Not(And(dp41, dp42, dp43)),
)

# It is possible to repeat the same digit twice, just make sure the two digits are not adjacent.
s.add(
    Not(And(dp11, dp12)),
    Not(And(dp21, dp22)),
    Not(And(dp31, dp32)),
    Not(And(dp41, dp42)),
    Not(And(dp12, dp13)),
    Not(And(dp22, dp23)),
    Not(And(dp32, dp33)),
    Not(And(dp42, dp43))
)

# a place only one digit and possible one place, one digit
s.add(
    AtMost(dp11, dp21, dp31, dp41, 1),  # position 1 (x1)
    Or(dp11, dp21, dp31, dp41),
    AtMost(dp12, dp22, dp32, dp42, 1),  # position 2 (x2)
    Or(dp12, dp22, dp32, dp42),
    AtMost(dp13, dp23, dp33, dp43, 1),  # position 3 (x3)
    Or(dp13, dp23, dp33, dp43)
)

# find a unique, there is exactly one possible 3-digit code that satisfies all the hints or only 1 solution is satisfies
if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("model: ", s.model())

    # or (vars != is_true), are there any possible result that differ from the previous result of the var(...)
    s.add(
        Or([
            var != is_true(model.evaluate(var, model_completion=True))
            for var in [dp11, dp21, dp31, dp41,
                        dp12, dp22, dp32, dp42,
                        dp13, dp23, dp33, dp43]
        ])
    )
    if s.check() == sat:
        print("not unique")
        print("second model:", s.model())
    else:
        print("unique")

else:
    print("unsatisfiable")
