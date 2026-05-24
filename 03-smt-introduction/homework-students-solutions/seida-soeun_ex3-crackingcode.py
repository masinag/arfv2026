from z3 import *

s = Solver()

# Exercise 3.4: Cracking the Code
# You are a hacker trying to break into a high-security system. You have to crack a
# password that is a 5-digit number. You know, from an anonymous source, that:
# - The 1st and last digits differ, as do the 2nd and 3rd.
# - The 2nd digit is twice the 1st, and the 4th is one less than the last.
# - No digit appears more than twice (e.g., 12322 is invalid).
# - The password cannot be sorted (e.g., 12279, 84321 are invalid).
# - The 1st and last digits are odd; the others are even.
# - The digits’ sum equals the 4th digit plus twice the 3rd.
# Crack the password using an SMT solver.
# Since you have only one guess you must be extremely careful. Is it the only solution?

digit1, digit2, digit3, digit4, digit5 = Ints("digit1 digit2 digit3 digit4 digit5")

# The 1st and last digits differ, as do the 2nd and 3rd.
# The 2nd digit is twice the 1st, and the 4th is one less than the last.
s.add(
    digit1 != digit5,
    digit2 != digit3,
    digit2 == digit1 * 2,
    digit4 == digit5 - 1
)

for digit in [digit1, digit2, digit3, digit4, digit5]:
    s.add(
        And(digit > 0, digit <= 9),
    )

# No digit appears more than twice (e.g., 12322 is invalid).
for number in range(1, 10):
    s.add(
        Sum([If(digit == number, 1, 0) for digit in [digit1, digit2, digit3, digit4, digit5]]) <= 2
    )

# The password cannot be sorted (e.g., 12279, 84321 are invalid).
s.add(
    Not(And(digit1 >= digit2, digit2 >= digit3, digit3 >= digit4, digit4 >= digit5)),
    Not(And(digit1 <= digit2, digit2 <= digit3, digit3 <= digit4, digit4 <= digit5)),
)

# The 1st and last digits are odd; the others are even.
s.add(
    digit1 % 2 != 0,
    digit5 % 2 != 0,
    digit2 % 2 == 0,
    digit3 % 2 == 0,
    digit4 % 2 == 0,
)

# The digits’ sum equals the 4th digit plus twice the 3rd.
s.add(
    Sum([digit1, digit2, digit3, digit4, digit5]) == digit4 + 2 * digit3
)

if s.check() == sat:
    print("satisfiable")

    model = s.model()
    valid = [model.evaluate(digit) for digit in [digit1, digit2, digit3, digit4, digit5]]
    print("model: ", "".join(str(digit) for digit in valid))
    second_model = []
    for digit in [digit1, digit2, digit3, digit4, digit5]:
        value = model.evaluate(digit, model_completion=True)
        second_model.append(digit != value)
    s.add(Or(second_model))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        model2= s.model()
        valid2 = [model2.evaluate(digit) for digit in [digit1, digit2, digit3, digit4, digit5]]
        print("model2: ", "".join(str(digit) for digit in valid2))
else:
    print("unsatisfiable")
