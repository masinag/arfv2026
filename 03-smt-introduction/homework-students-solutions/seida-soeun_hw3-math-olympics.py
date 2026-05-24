from z3 import *

s = Solver()

# Homework 3.1: Math Olympics
# Find 3 digits a, b, c, not necessarily distinct, with a !=0 and c !=0 such that both abc
# and cba are multiples of 4.

a, b, c = Ints("a b c")

for digit in [a, b, c]:
    s.add(digit <= 9, digit >= 0)

s.add(
    a != 0,
    c != 0
)

abc = 100 * a + 10 * b + c
cba = 100 * c + 10 * b + a

s.add(abc % 4 == 0)
s.add(cba % 4 == 0)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("model: ")
    print(f"a: {model[a]}, b: {model[b]}, c: {model[c]}")
    print("abc:", model.evaluate(abc))
    print("cba:", model.evaluate(cba))
else:
    print("unsatisfiable")