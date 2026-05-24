from z3 import *

s = Solver()

# Exercise 4.1: Black Hat Hacker
# You want to access the UniTN database. Sadly the server is protected by a key.
# From reverse engineering you obtain this part of code executed by the machine:
# # the key is the concat of 3 32-bit numbers a, b and c
# assert isMultiple(a,5)
# assert a | b == 2022
# assert a- b > 1000
# assert isAverage(c, [a,b])
# assert a * c <= 0x0017c1cc
# login()
# You have only one opportunity to log in, can you guess the key?

a, b, c = BitVecs("a b c", 32)

s.add(a % 5 == 0)
s.add(a | b == 2022)
# UGT = >
s.add(UGT(a - b, 1000))
s.add(2 * c == a + b)
# ULE = <=
s.add(ULE(a * c, 0x0017c1cc))

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print(f"a: {model[a]}, b: {model[b]}, c: {model[c]}")

    s.add(Or(a != model[a], b != model[b], c != model[c]))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        print("second model:", s.model())
else:
    print("unsatisfiable")
